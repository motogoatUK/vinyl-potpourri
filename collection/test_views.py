from django.test import TestCase
from django.contrib.auth.models import User
from .models import Collection


class TestCollectionViews(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def setUp(self):
        """setup methods"""
        # Create a test user
        self.testuser = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_index_view(self):
        """ verifies get request contains index page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # check template used is correct
        self.assertTemplateUsed(response, 'index.html')
        # check view contains Collection context
        self.assertSetEqual(
            response.context['collection_list'], Collection.objects.all())

    def test_collection_view(self):
        response = self.client.get('/collection/1/')
        self.assertEqual(response.status_code, 200)
        # check template used is correct
        self.assertTemplateUsed(response, 'record/record_list.html')

    def test_add_collection(self):
        # test unauthenticated users are redirected to login
        response = self.client.get('/collection/add/')
        self.assertRedirects(response,
                             '/accounts/login/?next=/collection/add/',
                             status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

    def test_add_collection_loggedin(self):
        self.client.force_login(self.testuser)
        # test new users can create a collection
        response = self.client.get('/collection/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
