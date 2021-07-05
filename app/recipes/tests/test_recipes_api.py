from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipes.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Empanadas',
        'description': 'Test description to prepare meat empanadas!'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)

class RecipesTests(TestCase):
    """Test recipes API access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """ Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateNotUsed(res.data, serializer.data)

