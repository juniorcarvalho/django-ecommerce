from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail


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
        self.url = reverse('contact')
        self.response = Client().get(self.url)
        self.data = {'name': 'Júnior', 'email': 'joseadolfojr@gmail.com', 'message': 'mensagem teste'}

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'contact.html')

    def test_form_error(self):
        data = {'name': '', 'email': '', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_form_ok(self):
        response = self.client.post(self.url, self.data)
        self.assertTrue(response.context['success'])

    def test_form_send_email(self):
        self.client.post(self.url, self.data)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Contato')




