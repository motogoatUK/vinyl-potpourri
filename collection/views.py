from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from my_profile.models import My_Profile

from .forms import CollectionForm
from .models import Collection
from record.models import Record


class CollectionList(generic.ListView):
    model = Collection


def index(request):
    collection_list = Collection.objects.all()
    context = {"collection_list": collection_list}
    return render(request, 'index.html', context)


def view_collection(request, id):
    """
    Gets a list of records from collection
    and sends them to the template
    """
    record_list = Record.objects.filter(collection=id)
    collection = get_object_or_404(Collection, pk=id)
    template = 'record/record_list.html'
    context = {
        "object_list": record_list,
        "collection": collection
    }
    return render(
        request, template, context
    )


@login_required
def add_collection(request):
    """ Add a new collection """
    profile = get_object_or_404(My_Profile, user=request.user)
    current_collections = Collection.objects.filter(username=profile.id)

    #  only users without a current collection
    #  and premium users are allowed to add a collection
    if current_collections and not profile.premium:
        messages.warning(
            request,
            'Sorry, only premium users can have more than one collection.'
            )
        return redirect(reverse('my_profile'))

    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            # add current user to form
            myform = form.save(commit=False)
            myform.username_id = profile.id
            myform.save()
            messages.success(request, 'Successfully added Collection!')
            return redirect('collections')
        else:
            messages.error(request, 'Failed to add Collection.')
    else:
        form = CollectionForm()

    template = 'collection/add-collection.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
