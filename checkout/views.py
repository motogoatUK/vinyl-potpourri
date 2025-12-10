import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import OrderForm
from .models import Product
from my_profile.models import My_Profile


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # load product info for the dropdown
    products = Product.objects.order_by('price')

    if request.method == 'GET':
        # Create initial form
        try:
            profile = My_Profile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'town_or_city': profile.default_town_or_city,
                'county': profile.default_county,
                'postcode': profile.default_postcode,
                'country': profile.default_country,
            })
        except My_Profile.DoesNotExist:
            order_form = OrderForm()

        # use first product to calculate initial payment intent
        product = products.first()

    if request.method == 'POST':
        # Get selected product
        item_sku = request.POST.get("item")
        product = Product.objects.get(sku=item_sku)
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
            'items': item_sku,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.save()
            return redirect(
                reverse('checkout_success', args=[order.order_number])
                )

        else:
            messages.error(request, 'There was an error with your form.'
                                    ' Please check your information.')

    # create payment intent for display
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(product),
        currency='gbp'
    )

    context = {
        'form': order_form,
        'product': products,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def calculate_order_amount(product):
    #     # Calculate the order total on the server to prevent
    #     # people from directly manipulating the amount on the client
    return int(product.price * 100)  # pence
