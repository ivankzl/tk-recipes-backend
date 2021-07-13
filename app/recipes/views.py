# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework import viewsets, mixins
from core.models import Ingredient, Recipe

from recipes import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe in the DB"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class

    def get_queryset(self):
        """
        Optionally restricts the returned recipes by
        filtering against a partial name
        """
        queryset = Recipe.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()
