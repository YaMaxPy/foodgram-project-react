from recipes.models import AmountIngredient


def recipe_amount_ingredients_set(recipe, ingredients):
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )
