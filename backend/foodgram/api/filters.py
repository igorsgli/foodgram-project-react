from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.MultipleChoiceFilter(
        'tags__slug',
        conjoined=False,
        choices=[
            ('breakfast', 'завтрак'),
            ('lunch', 'обед'),
            ('dinner', 'ужин')
        ],
        distinct=True
    )
    is_favorited = filters.CharFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.CharFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        if value in ('0', '1'):
            if value == '1':
                return queryset.filter(favorites__user=self.request.user)
            return queryset.exclude(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value in ('0', '1'):
            if value == '1':
                return queryset.filter(shoppingcarts__user=self.request.user)
            return queryset.exclude(shoppingcarts__user=self.request.user)
        return queryset
