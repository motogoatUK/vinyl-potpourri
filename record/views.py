from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from record.utils import get_ordering
from collection.models import Collection
from about.models import About
from .models import Artist, Record
from .forms import RecordForm


def index(request):
    return HttpResponse("Hello, records!")


class RecordList(generic.ListView):
    """
    Returns a Listview of records, using a queryset from the model
    which doesn't contain any hidden records unless they belong to
    the owner of the collection. Allows for field ordering.
    """
    model = Record

    def get_queryset(self):
        ordering = get_ordering(self.request, Record)
        queryset = Record.objects.visible(self.request.user)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


def artist_autocomplete(request):
    """
    Returns a JSON response containing Artist objects
    based on incoming query 'q'
    """
    q = request.GET.get("q", "")
    results = []
    if q:
        # Limit results to 10
        artists = Artist.objects.filter(name__icontains=q)[:10]
        results = [{"id": a.id, "name": a.name} for a in artists]
    return JsonResponse(results, safe=False)


def view_record(request, slug):
    """ returns record object from slug """
    queryset = Record.objects.all()
    record = get_object_or_404(queryset, slug=slug)
    # check if hidden
    if (not record.hide_record or
            request.user == record.collection.username.user):
        template = 'record/record.html'
        context = {
            "record": record,
        }
        return render(
            request, template, context
        )
    else:
        messages.error(request, 'That record is hidden from view by the owner')
        if (request.META.get('HTTP_REFERER')):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # or 403 if no referrer
        raise PermissionDenied


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
        # set message and send user back to referring page
        messages.error(request, 'record is not in your collection')
        if (request.META.get('HTTP_REFERER')):
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
    referrer = (request.META.get('HTTP_REFERER'))
    profile = request.user.my_profile
    about = About.objects.order_by("updated_on").last()
    free_tier = about.free_tier_records if about else 10
    # check eligibilty to add record
    if not (profile.premium or profile.num_records < free_tier):
        messages.error(request, 'Free record limit reached.')
        if referrer:
            return HttpResponseRedirect(referrer)
        else:
            return redirect('home')
    # check user has a collection to add records to
    collection = Collection.objects.filter(username__user=request.user)
    if not collection.exists():
        messages.error(request,
                       "You don't have any collections to add records"
                       " to yet. Please add one.")
        return redirect('my_profile')

    if request.method == 'POST':
        form = RecordForm(
            request.POST,
            request.FILES,
            user=request.user)
        if form.is_valid():
            record = form.save(commit=False)
            # pre-add a slug
            record.slug = slugify(record.a_side)
            record.artist = form.cleaned_data.get('artist')
            record.location = form.cleaned_data.get('location')
            record.save()
            record.slug = f"{record.slug}-{record.id}"
            record.save(update_fields=['slug'])
            # +1 to records created and add success message
            # profile = request.user.my_profile
            profile.num_records += 1
            profile.save()
            messages.success(request, 'Successfully added Record!')
            # return user to view the added record.
            return redirect('view_record', slug=record.slug)
        else:
            messages.error(request, 'Failed to add Record.')
    else:
        # get initial collection from URL
        collection = request.GET.get("collection")
        if collection:
            # Convert to int
            collection_id = int(collection)
            form = RecordForm(user=request.user, collection_id=collection_id)
        else:
            form = RecordForm(user=request.user)

    template = 'record/edit-record.html'
    context = {
        'form': form,
        'head_tag': 'Add',
        'submit_text': 'Add Record',
    }
    return render(request, template, context)


@login_required
def delete_record(request, slug):
    """
    function to delete a record
    """
    queryset = Record.objects.all()
    doomed_record = get_object_or_404(queryset, slug=slug)
    # Check the record is the users collection
    if doomed_record.collection.username.user == request.user:
        doomed_record.delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        # remove 1 from users num_records
        profile = request.user.my_profile
        profile.num_records -= 1
        profile.save()
        # Send user back to collection list as record will no longer exist
        return redirect('view_collection', id=doomed_record.collection_id)
    else:
        # send user back to referring page with error
        if (request.META.get('HTTP_REFERER')):
            messages.error(request, 'That record is not in your collection')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # or 403 if no referrer
        raise PermissionDenied
