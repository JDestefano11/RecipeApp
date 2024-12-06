from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name="Salt",
            quantity=1,
            unit="tsp"
        )
    
    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), "Salt (1 tsp)")
