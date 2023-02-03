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


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, RecipeTagInline)
    exclude = ('tags',)

    list_display = (
        'id', 'author', 'name', 'count_favorites', 'ingredients_list'
    )
    list_filter = ('author', 'tags', 'ingredients')
    search_fields = ('name',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Кол-во добавлений в избранное'

    def ingredients_list(self, obj):
        return [str(ingredient) for ingredient in obj.ingredients.all()]

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
