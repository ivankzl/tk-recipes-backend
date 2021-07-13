from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe object"""
    ingredients = IngredientSerializer(
        many=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        new_ingredient_pks = []

        recipe = super().update(instance, validated_data)

        for ingredient in ingredients_data:
            new_ingredient, created = recipe.ingredients.get_or_create(name=ingredient['name'])
            new_ingredient_pks.append(new_ingredient.id)

        recipe.ingredients.exclude(pk__in=new_ingredient_pks).delete()

        return recipe
