from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import User, Product
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name',  'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class ProductAdmin(admin.ModelAdmin):

    list_display = ('title', 'price', 'image', 'image_show')
    list_filter = ('title', 'price')
    search_fields = ('title', 'price')

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='50' />".format(obj.image.url))
        return None




admin.site.register(User, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
