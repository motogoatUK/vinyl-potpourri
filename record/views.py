from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render
from .models import Record


def index(request):
    return HttpResponse("Hello, records!")


class RecordList(generic.ListView):
    model = Record
