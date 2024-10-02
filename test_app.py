import unittest
import json
from app import app  # Импортируйте ваше Flask приложение


class ProductAPITestCase(unittest.TestCase):
    def setUp(self):
        """Создание тестового клиента и очистка базы данных перед каждым тестом."""
        self.app = app.test_client()
        self.app.testing = True

    def test_create_product(self):
        """Тестирование создания продукта."""
        response = self.app.post('/product', json={
            'name': 'Apple',
            'brand': 'Brand A',
            'quantity': 100,
            'price': 1.5,
            'material': 'Fruit'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Apple', response.get_data(as_text=True))

    def test_get_products(self):
        """Тестирование получения списка продуктов."""
        response = self.app.get('/product')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

    def test_update_product(self):
        """Тестирование обновления продукта."""
        # Сначала создаем продукт для обновления
        self.app.post('/product', json={
            'name': 'Banana',
            'brand': 'Brand B',
            'quantity': 50,
            'price': 1.2,
            'material': 'Fruit'
        })

        # Теперь обновляем продукт
        response = self.app.put('/product/Banana', json={
            'name': 'Banana',
            'brand': 'Brand B',
            'quantity': 60,
            'price': 1.2,
            'material': 'Fruit'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        """Тестирование удаления продукта."""
        # Сначала создаем продукт для удаления
        self.app.post('/product', json={
            'name': 'Orange',
            'brand': 'Brand C',
            'quantity': 80,
            'price': 0.8,
            'material': 'Fruit'
        })

        # Теперь удаляем продукт
        response = self.app.delete('/product/Orange')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
