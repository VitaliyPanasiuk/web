from django.contrib import admin
from .models import Products, ShopCalls, Image , ShopCategory, ShopSubCategory, ShopCurrency, AuthUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import site
site.disable_action('delete_selected')


admin.site.site_header = 'Luxon'
admin.site.site_title = 'Luxon Admin'


class ProductImage(admin.TabularInline):
    model = Image


@admin.register(Products)
class productAdmin(admin.ModelAdmin):
    search_fields = ('название_позиции', 'name', 'название_позиции_укр', 'id')
    list_display = ('название_позиции', 'цена', 'валюта', 'количество',)
    list_filter = ('наличие', 'страна_производитель', )
    readonly_fields  = ('id',)
    fieldsets = (
        ('Названия позиций на разных языках', {
            'fields': ('название_позиции','название_позиции_укр', 'name', )
        }),
        ('Цена', {
            'fields': ('цена', 'валюта', 'скидка', )
        }),
        ('Информация о товаре', {
            'fields': ('наличие' ,'единица_измерения', 'минимальный_объем_заказа', 'страна_производитель', 'личные_заметки', 'image',)
        }),
        ('Опт', {
            'fields': ('оптовая_цена', 'минимальный_заказ_опт', )
        }),
        ('Описания на разных языках', {
            'fields': ('описание' ,'описание_укр', 'description',)
        }),
    )
    actions = ['delete_selected']
    inlines = [ProductImage]
    

@admin.register(ShopCalls)
class productAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    search_fields = ('phone_number', 'first_name', 'last_name')
    list_display = ('phone_number', 'first_name', 'timedate')
    readonly_fields  = ('first_name', 'last_name', 'phone_number', 'viewed_product', 'price', 'timedate',)
    exclude = ('id', )
    
@admin.register(ShopSubCategory)
class productAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    search_fields = ('subcategory_name_ru', 'subcategory_name_en', 'subcategory_name_uk',)
    list_display = ('subcategory_name_ru', 'subcategory_id')


@admin.register(ShopCategory)
class productAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    search_fields = ('category_name_ru', 'category_name_en', 'category_name_uk',)
    list_display = ('category_name_ru', 'id',)
    exclude = ('id', )


@admin.register(ShopCurrency)
class currencyAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    search_fields = ('date', 'usd_to_uah',)
    list_display = ('date', 'usd_to_uah',)
    exclude = ('id', )
