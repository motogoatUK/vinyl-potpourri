from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from my_profile.models import My_Profile
from record.utils import get_ordering

from .forms import CollectionForm
from .models import Collection, Location
from record.models import Record


class CollectionList(generic.ListView):
    """ returns all collections ordered by id """
    model = Collection
    ordering = ['id']


class MyCollection(generic.ListView):
    """ returns a users collections """
    def get_queryset(self):
        return Collection.objects.filter(username__user=self.request.user)


def index(request):
    """ returns the 8 newest collections to show on the homepage """
    collection_list = Collection.objects.order_by('-id')[:8]
    context = {"collection_list": collection_list}
    return render(request, 'index.html', context)


def view_collection(request, id):
    """
    Gets a list of records from collection
    and sends them to the template. Utilises the 'visible'
    queryset from records.model to hide record where applicable.
    """
    collection = get_object_or_404(Collection, pk=id)
    ordering = get_ordering(request, Record)
    record_list = (Record.objects.visible(request.user)
                   .filter(collection=id))
    if ordering:
        record_list = record_list.order_by(ordering)

    template = 'record/record_list.html'
    context = {
        "object_list": record_list,
        "collection": collection
    }
    return render(
        request, template, context
    )


def location_autocomplete(request):
    """ returns a JSON response containing Locations"""
    q = request.GET.get("q", "")
    results = []
    if q:
        location = Location.objects.filter(name__icontains=q)[:10]
        results = [{"id": a.id, "name": a.name} for a in location]
    return JsonResponse(results, safe=False)


@login_required
def add_collection(request):
    """
    Add a new collection - only users without a current collection
    and premium users are allowed to add a collection
    """
    profile = get_object_or_404(My_Profile, user=request.user)
    current_collections = Collection.objects.filter(username=profile.id)

    if current_collections and not profile.premium:
        messages.warning(
            request,
            'Sorry, only premium users can have more than one collection.'
            )
        return redirect(reverse('my_profile'))

    if request.method == 'POST':
        form = CollectionForm(request.POST,
                              request.FILES)
        if form.is_valid():
            # add current user to form
            myform = form.save(commit=False)
            myform.username_id = profile.id
            myform.save()
            messages.success(request, 'Successfully added Collection!')
            return redirect('my_collection')
        else:
            messages.error(request, 'Failed to add Collection.')
    else:
        form = CollectionForm(userp=profile.premium)

    template = 'collection/add-collection.html'
    context = {
        'form': form,
        'head_tag': 'Add',
        'submit_text': 'Add Collection',
    }
    return render(request, template, context)


def edit_collection(request, id):
    """
    returns a form containing the collection data for editing
    Use same template as add_collection by adding extra context
    """
    collection = get_object_or_404(Collection, pk=id)
    if request.user == collection.username.user:
        if request.method == 'POST':
            form = CollectionForm(request.POST,
                                  request.FILES,
                                  instance=collection)
            if form.is_valid():
                myform = form.save(commit=False)
                # only update selected fields from form
                myform.save(update_fields=['name', 'description', 'image'])
                messages.success(request, 'Successfully modified Collection!')
                return redirect('collections', pk=id)
            else:
                messages.error(request, 'Failed to modify Collection.')
        else:
            form = CollectionForm(instance=collection,
                                  userp=collection.username.premium)

        template = 'collection/add-collection.html'
        context = {
            'form': form,
            'head_tag': 'Edit',
            'submit_text': 'Save Changes',
        }
        return render(request, template, context)
    else:
        if request.META.get('HTTP_REFERER'):
            # send user back to referring page with error
            messages.error(request, 'That collection is not yours!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # or 403 if no referrer
        raise PermissionDenied


@login_required
def delete_collection(request, id):
    """
    function to delete a record
    """
    queryset = Collection.objects.all()
    doomed = get_object_or_404(queryset, id=id)
    # Check the collection belongs to the user
    if doomed.username.user == request.user:
        # get number of records in collection and update users profile
        num_records = doomed.record_set.count()
        if num_records > 0:
            profile = request.user.my_profile
            profile.num_records -= num_records
            profile.save()
        doomed.delete()
        messages.success(request, f'"{doomed}" deleted!')
        messages.success(request, f'{num_records} records were also deleted.')
        # Send user back to collection list as collection will no longer exist
        return redirect('collections')
    else:
        # send user back to referring page with error
        if (request.META.get('HTTP_REFERER')):
            messages.error(request, f'"{doomed}" is not your collection')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # or 403 if no referrer
        raise PermissionDenied
