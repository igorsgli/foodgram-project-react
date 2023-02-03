from django.contrib import admin

from users.models import CustomUser


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
        return obj.recipes.count()

    count_recipes.short_description = 'Кол-во рецептов'

    def count_subscribers(self, obj):
        return obj.subscribed_by.count()

    count_subscribers.short_description = 'Кол-во подписчиков'
