from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(verbose_name='Название тега',
                            max_length=200,
                            unique=True)
    color = models.CharField(verbose_name='Цвет',
                             max_length=7,
                             unique=True)
    slug = models.SlugField(verbose_name='Слаг тега',
                            unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Единицы измерения',
                                        max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор рецепта',
                               on_delete=models.CASCADE,
                               related_name='recipes',)
    name = models.CharField(verbose_name='Название рецепта',
                            max_length=200)
    text = models.TextField(verbose_name='Описание рецепта',)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    image = models.ImageField(upload_to='recipes/',)
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Теги',
                                  related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='AmountIngredient',
                                         verbose_name='Ингредиенты',
                                         related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, message=('Время приготовления должно быть '
                                          'не меньше 1 минуты'))
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='amounts')
    ingredients = models.ForeignKey(Ingredient,
                                    verbose_name='Ингредиент',
                                    on_delete=models.CASCADE,
                                    related_name='amounts')
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(1, message='Количество не может быть меньше 1')]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe',)
        constraints = [
            models.UniqueConstraint(fields=['ingredients', 'recipe'],
                                    name='unique_ingredients_amount')
        ]

    def __str__(self):
        return f'{self.ingredients} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='shopping_carts')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='shopping_carts')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
