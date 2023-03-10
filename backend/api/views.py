from http import HTTPStatus

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow, User
from .filters import IngredientSearchFilter
from .mixins import AddDelViewMixin
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (CustomUserSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet, AddDelViewMixin):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    add_serializer = ShortRecipeSerializer

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        if self.request.user.is_anonymous:
            return queryset
        is_in_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_in_cart in ('1', 'true'):
            queryset = queryset.filter(shopping_carts__user=self.request.user)
        elif is_in_cart in ('0', 'false'):
            queryset = queryset.exclude(shopping_carts__user=self.request.user)
        is_favorite = self.request.query_params.get('is_favorited')
        if is_favorite in ('1', 'true'):
            queryset = queryset.filter(favorites__user=self.request.user)
        if is_favorite in ('0', 'false'):
            queryset = queryset.exclude(favorites__user=self.request.user)
        return queryset

    @action(methods=['GET', 'POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        return self._add_del_obj(pk, Favorite, Q(recipe__id=pk))

    @action(methods=['GET', 'POST', 'DELETE'],
            detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self._add_del_obj(pk, ShoppingCart, Q(recipe__id=pk))

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = AmountIngredient.objects.filter(
            recipe__shopping_carts__user=request.user).values_list(
            'ingredients__name', 'ingredients__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {'measurement_unit': item[1],
                                    'amount': item[2]}
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('HelveticaRegular', 'data/HelveticaRegular.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('HelveticaRegular', size=24)
        page.drawString(200, 800, 'Список покупок:')
        page.setFont('HelveticaRegular', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'''{i}. {name} - {data['amount']} '''
                                         f'''{data['measurement_unit']}'''))
            height -= 25
        page.showPage()
        page.save()
        return response


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=HTTPStatus.BAD_REQUEST
            )
        if Follow.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=HTTPStatus.BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=HTTPStatus.CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Follow.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=HTTPStatus.BAD_REQUEST
        )


class FollowListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (DjangoModelPermissions,)
