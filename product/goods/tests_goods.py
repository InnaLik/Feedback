import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from goods.models import Products


@pytest.mark.django_db
class ProductViewTest(TestCase):
    # def setUp(self):
    #     """Создаем тестовый товар для проверки представления"""
    #     self.product = Products.objects.create(
    #         name='Test Product',
    #         slug='test-product',
    #         description='Test product description',
    #         price=100
    #     )
    @classmethod
    def setUpTestData(cls):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  # Пустой файл
        cls.product = Products.objects.create(
            name='Test Product', slug='test-product', description='Test product description', price=100.0, image=image
        )

    def test_product_view_status_code(self):
        """Проверка правильности кода состояния (200) при правильном запросе"""
        url = reverse('catalog:get_product', kwargs={'product_slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_view_template(self):
        """Проверка, что используется правильный шаблон"""
        url = reverse('catalog:get_product', kwargs={'product_slug': self.product.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'goods/product.html')

    def test_product_view_404_for_invalid_slug(self):
        """Проверка генерации 404 ошибки при запросе несуществующего товара"""
        url = reverse('catalog:get_product', kwargs={'product_slug': 'non-existent-product'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
