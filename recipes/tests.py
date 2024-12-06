from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from categories.models import Category

class RecipeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test category
        cls.category = Category.objects.create(
            name='Main Course'
        )
        
        # Create test recipe
        cls.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='A test recipe description',
            cooking_time=30,
            difficulty='Easy',
            category=cls.category
        )

    def setUp(self):
        self.client = Client()

    def test_recipe_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipe_model(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.difficulty, 'Easy')
        self.assertEqual(self.recipe.category.name, 'Main Course')

    def test_recipe_search(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipe-search'), {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search.html')
