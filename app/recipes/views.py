# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework import viewsets, mixins
from core.models import Ingredient, Recipe

from recipes import serializers


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage ingredients in the DB"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    """Manage recipe in the DB"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()
