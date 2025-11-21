from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Record


def index(request):
    return HttpResponse("Hello, records!")


class RecordList(generic.ListView):
    model = Record


def view_record(request, slug):
    queryset = Record.objects.all()
    record = get_object_or_404(queryset, slug=slug)
    template = 'record/record.html'
    context = {
        "record": record,
    }
    return render(
        request, template, context
    )
