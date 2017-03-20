from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from model_mommy import mommy


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')
        self.response = Client().get(self.url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_template_use(self):
        self.assertTemplateUsed(self.response, 'accounts/register.html')

    def test_register_ok(self):
        data = {
            'username': 'teste',
            'email': 'joseadolfojr@gmail.com',
            'password1': 'brta@928',
            'password2': 'brta@928'
        }
        response = self.client.post(self.url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEquals(get_user_model().objects.count(), 1)

    def test_register_error(self):
        data = {
            'username': 'teste',
            'password1': 'brta@928',
            'password2': 'brta@928'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdateUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

        self.client.login(username=self.user.username, password='123')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_update_template_use(self):
        self.client.login(username=self.user.username, password='123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/update_user.html')
        self.client.logout()

    def test_update_user_ok(self):
        self.client.login(username=self.user.username, password='123')

        data = {'name': 'test', 'email': 'test@test.com'}
        response = self.client.post(self.url, data)
        accounts_index_url = reverse('accounts:index')
        self.assertRedirects(response, accounts_index_url)

        user = get_user_model().objects.get(username=self.user.username)
        self.assertEquals(user.email, 'test@test.com')
        self.assertEquals(user.name, 'test')

    def test_update_user_error(self):
        self.client.login(username=self.user.username, password='123')

        data = {}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdatePasswordTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

        self.client.login(username=self.user.username, password='123')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_update_template_use(self):
        self.client.login(username=self.user.username, password='123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/update_password.html')
        self.client.logout()

    def test_update_password_ok(self):
        self.client.login(username=self.user.username, password='123')
        data = {'old_password': '123', 'new_password1': 'maria@xyz', 'new_password2': 'maria@xyz'}
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('maria@xyz'))
