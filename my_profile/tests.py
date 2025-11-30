from django.test import TestCase
from django.contrib.auth.models import User
from my_profile.models import My_Profile


class TestMy_Profile(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def test_profile_signal(self):
        # Tests that a my_profile is created when a user is added
        username = 'testuser'
        User.objects.create_user(username, password='securepass1')
        # check profile has been created
        profile = My_Profile.objects.get(name=username)
        # check that the profile name matches username
        self.assertEqual(username, profile.name)
