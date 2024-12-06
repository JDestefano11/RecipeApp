from django.test import TestCase
from .models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Desserts")
    
    def test_category_str(self):
        self.assertEqual(str(self.category), "Desserts")
