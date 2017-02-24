from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ecommerce.catalog.models import Category, Product
#from model_mommy import mommy


class ProductListTestCase(TestCase):
    def setUp(self):
        self.url = reverse('catalog:product_list')
        self.response = Client().get(self.url)

    def tearDown(self):
        Product.objects.all().delete()

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_use(self):
        self.assertTemplateUsed(self.response, 'catalog/product_list.html')

    def test_context(self):
        self.assertTrue('product_list' in self.response.context)

    # def test_context_content(self):
    #     mommy.make(Product)
    #     response = self.client.get(self.url)
    #     product_list = response.context['product_list']
    #     self.assertEquals(product_list.count(), 1)




