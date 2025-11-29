from django.test import TestCase
from .models import Record


class TestRecordViews(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def test_record_list(self):
        """ verifies get request contains record_list """
        response = self.client.get('/record/')
        self.assertEqual(response.status_code, 200)
        # check template used is correct
        self.assertTemplateUsed(response, 'record/record_list.html')
        # check view contains Collection context
        self.assertSetEqual(
            response.context['record_list'], Record.objects.all())

    def test_record_view(self):
        # Thanks to
        record = Record.objects.first()
        slug = record.slug
        response = self.client.get(f'/record/{slug}/')
        self.assertEqual(response.status_code, 200)
        # check template used is correct
        self.assertTemplateUsed(response, 'record/record.html')
