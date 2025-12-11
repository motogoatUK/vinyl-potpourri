import stripe
from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django_countries.fields import Country
from .forms import OrderForm
from .models import Order, Product
from my_profile.models import My_Profile
from my_profile.forms import FullProfileForm


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
        # save the users full name to User model's first name and last name
        full_name = request.POST.get('full_name', '').strip()
        # split the full name
        name_parts = full_name.split()
        # set first name if length > 0
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        # if length > 1 the set last name
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        # get the form data safely
        form_data = {
            'full_name': full_name,
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'county': request.POST.get('county', ''),
            'postcode': request.POST.get('postcode', ''),
            'country': request.POST.get('country', ''),
            'item': item_sku,
            }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # save names to User if they don't exist
            user = request.user
            if not user.get_full_name():
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            # save the order
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.order_total = product.price
            order.save()
            request.session['save_info'] = 'save-info' in request.POST
            request.session['checkout_complete'] = True
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
    # Calculate the order total on the server to prevent
    # any manipulation of the amount on the client
    return int(product.price * 100)  # pence


def checkout_success(request, order_number):
    """
    successful checkout routine
    will only be displayed directly from checkout
    by checking the session flag
    """
    if not request.session.get('checkout_complete'):
        messages.error(request,
                       "You cannot access the checkout success page directly.")
        return redirect('home')
    # now reset the flag in a try block to avoid and key errors
    # https://docs.djangoproject.com/en/dev/topics/http/sessions/
    try:
        del request.session['checkout_complete']
    except KeyError:
        pass
    # get the data
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    # Attach the user's profile to the order
    if request.user.is_authenticated:
        profile = My_Profile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()
        # Save the users default info to their profile
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': Country(order.country).code if
                order.country else None,
            }
            user_profile_form = FullProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
            else:
                messages.error(request, user_profile_form.errors)
        # Handle upgrading user account
        plan_months = int(request.GET.get("months", 3))
        today = date.today()
        # If existing exp_date is in the future, extend from it.
        if profile.exp_date and profile.exp_date > today:
            start_date = profile.exp_date
        else:
            start_date = today
        # Add months (3, 6, 12)
        new_exp_date = start_date + relativedelta(months=plan_months)
        # Update fields
        profile.premium = True
        profile.sub_date = today
        profile.exp_date = new_exp_date
        profile.save()

    messages.success(request, (
        f'Order successfully processed!'
        f'Your order number is {order_number}. A confirmation'
        f' email will be sent to {order.email}.')
                     )
    template = 'checkout/checkout-success.html'
    context = {
        'order': order,
        'save_info': save_info,
        'exp_date': new_exp_date
    }

    return render(request, template, context)
