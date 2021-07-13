from django.contrib import admin
from .models import Продукт, Заказ, orderItems


def make_order_done(modeladmin, request, queryset):
    queryset.update(статус_заказа='d')
make_order_done.short_description = "Заказ выполнен"

def make_order_undone(modeladmin, request, queryset):
    queryset.update(статус_заказа='nd')
make_order_undone.short_description = "Отменить выполнение заказа"


admin.site.site_header = 'Luxon'
admin.site.site_title = 'Luxon Admin'

@admin.register(Продукт)
class productAdmin(admin.ModelAdmin):
    search_fields = ('название_позиции',)
    list_display = ('название_позиции', 'цена', 'валюта', 'количество',)
    list_filter = ('наличие', 'страна_производитель', )
    readonly_fields  = ('id',)

@admin.register(orderItems)
class orderItemAdmin(admin.ModelAdmin):'''
    search_fields = ('фамилия', 'имя')
    list_display = ('id', 'имя' , 'фамилия', 'заказ', 'статус_заказа', 'статус_оплаты', 'дата_заказа')
    #filter_horizontal = ('заказ',)
    list_filter = ('статус_заказа', 'статус_оплаты', )
    readonly_fields  = ('id', 'user_id')
    actions = [make_order_done, make_order_undone]'''

@admin.register(Заказ)
class orderAdmin(admin.ModelAdmin):
    search_fields = ('фамилия', 'имя')
    list_display = ('id', 'имя' , 'фамилия', 'статус_заказа', 'статус_оплаты', 'дата_заказа')
    #filter_horizontal = ('заказ',)
    list_filter = ('статус_заказа', 'статус_оплаты', )
    readonly_fields  = ('id', 'user_id')
    actions = [make_order_done, make_order_undone]

