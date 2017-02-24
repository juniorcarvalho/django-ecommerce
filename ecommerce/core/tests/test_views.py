from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexViewTestCase(TestCase):
    def setUp(self):
        url = reverse('index')
        self.response = Client().get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'index.html')


class ContactViewTestCase(TestCase):
    def setUp(self):
        url = reverse('contact')
        self.response = Client().get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'contact.html')

