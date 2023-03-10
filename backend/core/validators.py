from django.core.exceptions import ValidationError

from recipes.models import Ingredient, Tag


def tags_exist_validator(tags_ids, Tag):
    exists_tags = Tag.objects.filter(id__in=tags_ids)
    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_exist_validator(ingredients, Ingredient):
    ings_ids = [None] * len(ingredients)
    for idx, ing in enumerate(ingredients):
        ingredients[idx]['amount'] = int(ingredients[idx]['amount'])
        if ingredients[idx]['amount'] < 1:
            raise ValidationError('Неправильное количество ингидиента')
        ings_ids[idx] = ing.pop('id', 0)

    ings_in_db = Ingredient.objects.filter(id__in=ings_ids).order_by('pk')
    ings_ids.sort()

    for idx, id in enumerate(ings_ids):
        ingredient: 'Ingredient' = ings_in_db[idx]
        if ingredient.id != id:
            raise ValidationError('Ингридент не существует')

        ingredients[idx]['ingredient'] = ingredient
    return ingredients
