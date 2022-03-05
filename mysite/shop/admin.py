from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from cart.models import Order, NotificationPeriod
from .models import User, Product, PromoCode
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'image', 'image_show', 'discount')
    list_editable = ('price', 'discount')
    list_filter = ('title', 'price')
    search_fields = ('title', 'price')

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='50' />".format(obj.image.url))
        return None


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'expiration_date', 'promo_discount', 'is_active', 'works_with_discount')
    list_editable = ('is_active', 'promo_discount', 'works_with_discount')
    search_fields = ('promo_code', 'expiration_date', 'promo_discount', 'is_active')
    list_display_links = ('promo_code', 'expiration_date')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date', 'cart', 'text', 'promo_code', 'final_amount', 'execution_date')
    search_fields = ('user', 'created_date', 'promo_code')
    list_display_links = ('user',)


class NotificationPeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'minutes',)
    list_editable = ('minutes',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(NotificationPeriod, NotificationPeriodAdmin)
