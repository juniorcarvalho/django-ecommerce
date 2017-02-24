from django.test import TestCase
from ecommerce.catalog.models import Category, Product
from model_mommy import mommy
from django.core.urlresolvers import reverse


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = mommy.make(Category)

    def test_get_absolute_url(self):
        self.assertEquals(self.category.get_absolute_url(),
                          reverse('catalog:category', kwargs={'slug': self.category.slug}))


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = mommy.make(Product)

    def test_get_absolute_url(self):
        self.assertEquals(self.product.get_absolute_url(),
                          reverse('catalog:product', kwargs={'slug': self.product.slug}))
