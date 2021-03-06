from django.db import models


class Recipe(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255, blank=False, default=None)
    description = models.TextField(blank=False, default=None)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for a recipe"""
    name = models.CharField(max_length=255, blank=False, default=None)
    recipe = models.ForeignKey(
        Recipe,
        related_name="ingredients",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
