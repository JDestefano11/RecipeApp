from django.db import models
from django.utils import timezone
from categories.models import Category
from ingredients.models import Ingredient

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.IntegerField()
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    ingredients = models.ManyToManyField(Ingredient)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # New fields
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    servings = models.IntegerField(default=1)

    def __str__(self):
        return self.name
