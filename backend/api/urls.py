from django.urls import include, path
from rest_framework import routers

from .views import (FollowListView, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet, UsersViewSet)

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
