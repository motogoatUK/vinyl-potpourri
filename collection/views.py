from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Collection
from record.models import Record


class CollectionList(generic.ListView):
    model = Collection


def view_collection(request, id):
    """
    Gets a list of records from collection
    and sends them to the template
    """
    record_list = Record.objects.filter(collection__in=id)
    collection = get_object_or_404(Collection, pk=id)
    template = 'record/record_list.html'
    context = {
        "object_list": record_list,
        "collection": collection
    }
    return render(
        request, template, context
    )
