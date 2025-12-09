from django.shortcuts import render
from .models import About
from checkout.models import Product


def about_us(request):
    """
    Renders the most recent About-us page
    Template: `about/about-us.html`
    """
    # get the latest updated content
    about = About.objects.order_by("updated_on").last()
    # get the product info
    product = Product.objects.order_by('price')
    context = {'about': about,
               'product': product,
               }

    return render(request, "about/about-us.html", context)
