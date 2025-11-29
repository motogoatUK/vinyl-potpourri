from django.test import TestCase
from .models import Collection


class TestCollectionViews(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def setUp(self):
        """setup methods"""

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
