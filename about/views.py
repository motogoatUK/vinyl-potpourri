from django.shortcuts import render
from .models import About


def about_us(request):
    """
    Renders the most recent About-us page
    Template: `about/about-us.html`
    """
    # get the latest updated content
    about = About.objects.order_by("updated_on").last()
    context = {'about': about, }

    return render(request, "about/about-us.html", context)
