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
        response = self.app.post('/products/', json={  # Измените здесь на /products/
            'name': 'Apple',
            'manufacturer': 'Brand A',  # Измените здесь на manufacturer
            'quantity': 100,
            'price': 1.5,
            'date_added': '2024-10-01'  # Добавьте поле date_added
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Apple', response.get_data(as_text=True))

    def test_get_products(self):
        """Тестирование получения списка продуктов."""
        response = self.app.get('/products/')  # Измените здесь на /products/
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

    def test_update_product(self):
        """Тестирование обновления продукта."""
        # Сначала создаем продукт для обновления
        create_response = self.app.post('/products/', json={  # Измените здесь на /products/
            'name': 'Banana',
            'manufacturer': 'Brand B',  # Измените здесь на manufacturer
            'quantity': 50,
            'price': 1.2,
            'date_added': '2024-10-01'  # Добавьте поле date_added
        })
        product_id = create_response.json['id']  # Получаем ID созданного продукта

        # Теперь обновляем продукт
        response = self.app.put(f'/products/{product_id}', json={  # Используйте /products/{id}
            'name': 'Banana',
            'manufacturer': 'Brand B',
            'quantity': 60,
            'price': 1.2,
            'date_added': '2024-10-01'  # Добавьте поле date_added
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        """Тестирование удаления продукта."""
        # Сначала создаем продукт для удаления
        create_response = self.app.post('/products/', json={  # Измените здесь на /products/
            'name': 'Orange',
            'manufacturer': 'Brand C',  # Измените здесь на manufacturer
            'quantity': 80,
            'price': 0.8,
            'date_added': '2024-10-01'  # Добавьте поле date_added
        })
        product_id = create_response.json['id']  # Получаем ID созданного продукта

        # Теперь удаляем продукт
        response = self.app.delete(f'/products/{product_id}')  # Используйте /products/{id}
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
