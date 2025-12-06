from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Artist, Record
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


def artist_autocomplete(request):
    q = request.GET.get("q", "")
    results = []

    if q:
        artists = Artist.objects.filter(name__icontains=q)[:10]
        results = [{"id": a.id, "name": a.name} for a in artists]

    return JsonResponse(results, safe=False)


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


@login_required
def edit_record(request, slug):
    """
    edit_record
    provides pre-filled record form after checking
    the record instance belongs to the user (via collection)
    """
    record = get_object_or_404(Record, slug=slug)

    if request.user == record.collection.username.user:
        if request.method == 'POST':
            form = RecordForm(
                request.POST,
                request.FILES,
                instance=record, user=request.user)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.artist = form.cleaned_data.get('artist')
                myform.location = form.cleaned_data.get('location')
                myform.save()
                messages.success(request, 'Successfully modified Record!')
                return redirect('view_collection', id=record.collection_id)
            else:
                messages.error(request, 'Failed to modify Record.')
        else:
            form = RecordForm(instance=record, user=request.user)

        template = 'record/edit-record.html'
        context = {
            'form': form,
            'head_tag': 'Edit',
            'submit_text': 'Save Changes',
        }
        return render(request, template, context)

    else:
        # send user back to referring page with error
        if (request.META.get('HTTP_REFERER')):
            messages.error(request, 'record is not in your collection')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # or 403 if no referrer
    raise PermissionDenied


@login_required
def add_record(request):
    """
    Add a record to the database. If NOT premium then limit to 10 records
    Template: edit-record
    Add vars to context
    """
    # if request.user__profile.premium:
    if request.method == 'POST':
        form = RecordForm(
            request.POST,
            request.FILES,
            user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.artist = form.cleaned_data.get('artist')
            myform.location = form.cleaned_data.get('location')
            record = myform.save()
            messages.success(request, 'Successfully added Record!')
            return redirect('view_collection', id=record.collection_id)
        else:
            messages.error(request, 'Failed to add Record.')
    else:
        form = RecordForm(user=request.user)

    template = 'record/edit-record.html'
    context = {
        'form': form,
        'head_tag': 'Add',
        'submit_text': 'Add Record',
    }
    return render(request, template, context)

    # else:
    #     # send user back to referring page with error
    #     if (request.META.get('HTTP_REFERER')):
    #         messages.error(request, 'record is not in your collection')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #     # or 403 if no referrer
    # raise PermissionDenied
