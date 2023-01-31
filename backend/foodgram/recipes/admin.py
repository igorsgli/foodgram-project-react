from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Subscription,
    Tag
)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    verbose_name = 'fjlsjfs'


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeTagInline)
    exclude = ('tags',)

    list_display = (
        'id', 'author', 'name', 'count_favorites', 'ingredients_list'
    )
    list_filter = ('author', 'tags', 'ingredients')
    search_fields = ('name',)

    def count_favorites(self, obj):
        from django.db.models import Count
        result = Favorite.objects.filter(
            recipe=obj
        ).aggregate(count=Count('user'))
        return result['count']

    count_favorites.short_description = 'Кол-во добавлений в избранное'

    def ingredients_list(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return [str(ingredient) for ingredient in ingredients]

    ingredients_list.short_description = 'Ингредиенты'


admin.site.register(Recipe, RecipeAdmin)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
