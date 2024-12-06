from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
