from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthor
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    TagSerializer,
    RecipeCreateUpdateSerializer,
    RecipeMinifiedSerializer,
    RecipeListSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
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
from users.models import CustomUser


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
        queryset = CustomUser.objects.filter(
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
            'user': self.request.user.id,
            'author': author.id
        }
        if self.request.method ==    'POST':
            subscription_serializer = SubscriptionSerializer(data=kwargs)
            subscription_serializer.is_valid(raise_exception=True)
            subscription_serializer.save()

            context = self.get_serializer_context()
            serializer = self.get_serializer_class()
            return Response(
                serializer(instance=author, context=context).data,
                status=status.HTTP_201_CREATED
            )
        get_object_or_404(
            Subscription,
            author=id,
            user=self.request.user.id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_class = IngredientFilter

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return Ingredient.objects.filter(name__istartswith=name)
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_class = RecipeFilter

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

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        if self.action in ('favorite'):
            return FavoriteSerializer
        if self.action in ('shopping_cart'):
            return ShoppingCartSerializer
        return RecipeListSerializer

    @staticmethod
    def create_object(serializer, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        kwargs = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        object_serializer = serializer(data=kwargs)
        object_serializer.is_valid(raise_exception=True)
        object_serializer.save()
        return Response(
            RecipeMinifiedSerializer(instance=recipe).data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete_object(model, request, pk):
        get_object_or_404(
            model,
            recipe=pk,
            user=request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk=None):
        return self.create_object(self.get_serializer_class(), request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.delete_object(Favorite, request, pk)

    @action(methods=['post'], detail=True)
    def shopping_cart(self, request, pk=None):
        return self.create_object(self.get_serializer_class(), request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.delete_object(ShoppingCart, request, pk)

    @staticmethod
    def save_file(items):
        text = '\n'.join([
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) - {item['total']}"
            for item in items
        ])
        filename = 'shoping_cart.txt'
        response = HttpResponse(text, content_type='text/plain')
        print(f'attachment; filename={filename}')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        items = RecipeIngredient.objects.select_related(
            'recipe', 'ingredient'
        ).filter(
            recipe__shoppingcart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            total=Sum('amount')
        ).order_by('ingredient__name')
        # return self.save_file(items)
        text = '\n'.join([
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) - {item['total']}"
            for item in items
        ])
        filename = 'shoping_cart.txt'
        response = HttpResponse(text, content_type='text/plain')
        # print(f'attachment; filename={filename}')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
