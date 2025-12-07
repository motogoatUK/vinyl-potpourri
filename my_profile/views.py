from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from my_profile.models import My_Profile
from .forms import ProfileForm


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    """ use LoginRequiredMixin to redirect guests to the login page """
    model = My_Profile
    template_name = 'my_profile/my_profile.html'
    login_url = "/accounts/login/"
    context_object_name = 'profile'

    def get_object(self):
        """ get ONLY the current users profile """
        return get_object_or_404(
            My_Profile,
            user=self.request.user
        )


def edit_profile(request):
    profile = request.user.my_profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'my_profile/my_profile.html', {'form': form})
