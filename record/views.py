from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Record


def index(request):
    return HttpResponse("Hello, records!")


class RecordList(generic.ListView):
    model = Record

    def get_ordering(self):
        """
        Override to allow dynamic ordering
        via ?ordering=field or ?ordering=-field
        """
        ordering = self.request.GET.get("ordering", "title")

        if ordering:
            try:
                # Validate ordering field to prevent SQL injection
                if ordering.lstrip('-') in [
                        f.name for f in Record._meta.get_fields()]:
                    return ordering
            except ValueError:
                pass  # Ignore invalid ordering fields


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
