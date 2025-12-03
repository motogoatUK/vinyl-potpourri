from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Record
from .forms import RecordForm


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


def edit_record(request, slug):
    record = get_object_or_404(Record, slug=slug)

    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.notes = form.cleaned_data['notes']
            myform.save()
            messages.success(request, 'Successfully modified Record!')
            return redirect('view_collection', id=record.collection_id)
        else:
            print(form)
            messages.error(request, 'Failed to modify Record.')
    else:
        form = RecordForm(instance=record)

    template = 'record/edit-record.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
