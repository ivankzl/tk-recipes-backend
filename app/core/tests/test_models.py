from django.db import IntegrityError
from django.test import TestCase
from core import models


def sample_recipe(name='Banana bread', description='Test description'):
    """Create a sample recipe"""
    return models.Recipe.objects.create(name=name, description=description)


class ModelTests(TestCase):

    def test_create_recipe_with_name_and_description_successful(self):
        """Test create a new recipe with name and desc is successful"""
        name = 'Spaghetti carbonara'
        description = 'Test Description'

        recipe = sample_recipe(name, description)

        self.assertEqual(recipe.name, name)
        self.assertEqual(recipe.description, description)

    def test_create_invalid_recipe(self):
        """Test creating a recipe with no name"""

        with self.assertRaises(IntegrityError):
            models.Recipe.objects.create(description='Test description')

    def test_ingredient_str(self):
        """Test the ingrediente string representation"""
        recipe = sample_recipe()
        ingredient = models.Ingredient.objects.create(recipe=recipe, name='Milk')

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = sample_recipe('Banana bread', 'Test')

        self.assertEqual(str(recipe), recipe.name)
