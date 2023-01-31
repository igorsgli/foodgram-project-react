from django.contrib import admin

from users.models import CustomUser
from recipes.models import Recipe, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name',
        'count_recipes', 'count_subscribers'
    )
    search_fields = ('username',)
    list_filter = ('email', 'first_name',)

    def count_recipes(self, obj):
        from django.db.models import Count
        result = Recipe.objects.filter(author=obj).aggregate(count=Count('id'))
        return result['count']

    count_recipes.short_description = 'Кол-во рецептов'

    def count_subscribers(self, obj):
        from django.db.models import Count
        result = Subscription.objects.filter(
            author=obj
        ).aggregate(count=Count('user'))
        return result['count']

    count_subscribers.short_description = 'Кол-во подписчиков'
