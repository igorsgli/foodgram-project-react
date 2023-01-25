from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthor
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeCreateUpdateSerializer,
    RecipeMinifiedSerializer,
    RecipeListSerializer,
    UserSubscriptionsSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    RecipeIngredient,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action in ('subscribe', 'subscriptions'):
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('subscriptions', 'subscribe'):
            return UserSubscriptionsSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if (
            self.action in ('subscriptions')
            and self.request.method == 'GET'
        ):
            recipes_limit = self.request.query_params.get(
                'recipes_limit', settings.DEFAULT_RECIPES_LIMIT
            )
            context['recipes_limit'] = int(recipes_limit)
        return context

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscribed_by__user=self.request.user
        ).all()
        context = self.get_serializer_context()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer_class()(
            page,
            context=context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        author = get_object_or_404(self.get_queryset(), pk=id)
        kwargs = {
            'user': self.request.user,
            'author': author
        }
        if self.request.method == 'POST':
            try:
                Subscription.objects.create(**kwargs)
            except IntegrityError:
                raise ValidationError({'error': 'Подписка не получилась.'})
            context = self.get_serializer_context()
            serializer = self.get_serializer_class()
            return Response(
                serializer(instance=author, context=context).data,
                status=status.HTTP_201_CREATED
            )
        instance = Subscription.objects.filter(**kwargs).first()
        if instance is None:
            raise ValidationError({'errors': 'Подписка не существует.'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return Ingredient.objects.filter(name__istartswith=name)
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in (
            'favorite',
            'shopping_cart',
            'download_shopping_cart'
        ):
            return [IsAuthenticated()]
        if self.action in ('patch', 'destroy'):
            return [IsAuthor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        if self.action in ('favorite', 'shopping_cart'):
            return RecipeMinifiedSerializer
        return RecipeListSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()

        author = self.request.query_params.get('author')
        if author is not None:
            return queryset.filter(author=author)

        tags = self.request.query_params.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1':
            return queryset.filter(favorites__user=self.request.user)

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        if is_in_shopping_cart == '1':
            return queryset.filter(shopping_carts__user=self.request.user)

        return queryset

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(self.get_queryset(), pk=pk)
        kwargs = {
            'user': self.request.user,
            'recipe': recipe
        }
        if self.request.method == 'POST':
            try:
                Favorite.objects.create(**kwargs)
            except IntegrityError:
                raise ValidationError(
                    {'error': 'Рецепт не получилось добавить в избранное.'}
                )
            context = self.get_serializer_context()
            serializer = self.get_serializer_class()
            return Response(
                serializer(instance=recipe, context=context).data,
                status=status.HTTP_201_CREATED
            )
        instance = Favorite.objects.filter(**kwargs).first()
        if instance is None:
            raise ValidationError({'errors': 'Рецепта нет в избранном.'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(self.get_queryset(), pk=pk)
        kwargs = {
            'user': self.request.user,
            'recipe': recipe
        }
        if self.request.method == 'POST':
            try:
                ShoppingCart.objects.create(**kwargs)
            except IntegrityError:
                raise ValidationError(
                    {'error': 'Рецепт не получилось добавить в список покупок'}
                )
            context = self.get_serializer_context()
            serializer = self.get_serializer_class()
            return Response(
                serializer(instance=recipe, context=context).data,
                status=status.HTTP_201_CREATED
            )
        instance = ShoppingCart.objects.filter(**kwargs).first()
        if instance is None:
            raise ValidationError(
                {'errors': 'Рецепта нет в списке покупок.'}
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        items = RecipeIngredient.objects.select_related(
            'recipe', 'ingredient'
        ).filter(
            recipe__shopping_carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            name=F('ingredient__name'),
            units=F('ingredient__measurement_unit'),
            total=Sum('amount'),
        )

        text = '\n'.join([
            f"{item['name']} ({item['units']}) - {item['total']}"
            for item in items
        ])
        filename = 'shoping_cart.txt'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
