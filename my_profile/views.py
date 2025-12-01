from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from my_profile.models import My_Profile


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
