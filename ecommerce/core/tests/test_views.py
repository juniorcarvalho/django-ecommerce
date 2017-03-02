from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
from model_mommy import mommy


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


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.response = Client().get(self.url)
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'login.html')

    def test_login_ok(self):
        data = {'username': self.user.username, 'password': '123'}
        response = Client().post(self.url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_error(self):
        data = {'username': self.user.username, 'password': '1234'}
        response = Client().post(self.url, data)
        error_msg = ('Por favor, entre com um usuário  e senha corretos.'
                     ' Note que ambos os campos diferenciam maiúsculas e minúsculas.')
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', None, error_msg)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.response = Client().get(self.url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_templated_uset(self):
        self.assertTemplateUsed(self.response, 'register.html')

    def test_register_ok(self):
        data = {'username': 'teste', 'password1': 'brta@928', 'password2': 'brta@928'}
        response = self.client.post(self.url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEquals(get_user_model().objects.count(), 1)






