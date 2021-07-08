from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipes.serializers import RecipeSerializer

RECIPES_URL = reverse('recipes:recipe-list')


def recipe_detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipes:recipe-detail', args=[recipe_id])


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Empanadas',
        'description': 'Test description to prepare meat empanadas!'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


class PublicRecipesApiTest(TestCase):
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
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe()

        url = recipe_detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating a recipe without ingredients"""

        payload = {'name': 'Focaccia', 'description': 'Detailed description'}

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        self.assertEqual(payload['name'], recipe.name)
        self.assertEqual(payload['description'], recipe.description)

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with multiple ingredients"""

        payload = {
            'name': 'Gnocchi',
            'description': 'A detailed description of a yummy recipe!',
            'ingredients': [
                {'name': 'Potatoes'},
                {'name': 'Flour'},
                {'name': 'Nutmeg'}
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        self.assertEqual(payload['name'], recipe.name)
        self.assertEqual(payload['description'], recipe.description)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe()
        original_description = recipe.description
        payload = {'name': 'Panqueques con dulce de leche'}

        url = recipe_detail_url(recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, original_description)

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        recipe = sample_recipe()
        recipe.ingredients.create(name='Eggs')
        original_description = recipe.description

        payload = {
            'name': 'Vegan gnocchi',
            'ingredients': [{'name': 'Vegegg'}]
        }
        url = recipe_detail_url(recipe.id)
        self.client.put(url, payload, format='json')

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, original_description)
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertTrue(recipe.ingredients.first().name, 'Eggs')
