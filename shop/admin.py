from django.contrib import admin
from .models import Продукт, Заказ, ShopCalls, Image , ShopCategory, ShopSubCategory
from django.contrib.admin import site
site.disable_action('delete_selected')

def make_order_done(modeladmin, request, queryset):
    queryset.update(статус_заказа='d')
make_order_done.short_description = "Заказ выполнен"

def make_order_undone(modeladmin, request, queryset):
    queryset.update(статус_заказа='nd')
make_order_undone.short_description = "Отменить выполнение заказа"


admin.site.site_header = 'Luxon'
admin.site.site_title = 'Luxon Admin'

class ProductImage(admin.TabularInline):
    model = Image

'''class ShopSubCategoryAdmin(admin.StackedInline):
    model = ShopSubCategory
    extra = 1'''

@admin.register(Продукт)
class productAdmin(admin.ModelAdmin):
    search_fields = ('название_позиции', 'name', 'название_позиции_укр')
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
    #exclude = ('поисковые_запросы', 'поисковые_запросы_укр', 'ссылка_изображения', 'номер_группы', 'адрес_подраздела', 'возможность_поставки', 'тип_товара', 'код_товара',)

@admin.register(Заказ)
class orderAdmin(admin.ModelAdmin):
    search_fields = ('фамилия', 'имя')
    list_display = ('id', 'имя' , 'фамилия', 'confirm', 'статус_оплаты', 'дата_заказа')
    #filter_horizontal = ('заказ',)
    list_filter = ('confirm', 'статус_оплаты', )
    readonly_fields  = ('id', 'user_id')
    actions = [make_order_done, make_order_undone, 'delete_selected']
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('фамилия','имя', 'отчество', 'телефон', 'почта')
        }),
        ('Информация о заказе', {
            'fields': ('order_ru', 'сумма_заказа', 'валюта_заказа', 'статус_оплаты', 'confirm', 'дата_заказа')
        }),
        ('Адрес доставки', {
            'fields': ('delivery_type', 'payment_type', 'city', 'street', 'house', 'nova_pochta', 'ukr_pochta' )
        }),
    )
    exclude = ('заказ', )
    model = Заказ
    

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
    #inlines = [ShopSubCategoryAdmin]