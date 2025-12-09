from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OrderForm


@login_required
def checkout(request):
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {'form': order_form, }

    return render(request, template, context)
