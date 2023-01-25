from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', 'password'
    )
    list_editable = ('password',)
    search_fields = ('username',)
    list_filter = ('email', 'first_name',)
