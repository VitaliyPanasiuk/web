from django.contrib import admin
from .models import OrderItem, Orders
from fieldsets_with_inlines import FieldsetsInlineMixin


@admin.action(description='Заказ выполнен')
def make_order_done(modeladmin, request, queryset):
    queryset.update(confirm='done')

@admin.action(description='Заказ подтвержден администратором')
def make_order_confirmed_by_admin(modeladmin, request, queryset):
    queryset.update(confirm='ac')

@admin.action(description='Заказ не подтвержден пользователем')
def make_order_unconfirmed_by_user(modeladmin, request, queryset):
    queryset.update(confirm='unc')

@admin.action(description='Отправить заказ обратно в обработку')
def make_order_pending(modeladmin, request, queryset):
    queryset.update(confirm='uc')


class OrderItemTable(admin.TabularInline):
    model = OrderItem
    fields = ("name_ru", "amount", "price",)
    #readonly_fields = ("currency",)
    

@admin.register(Orders)
class orderAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    search_fields = ('last_name', 'first_name')
    list_display = ('id', 'first_name' , 'last_name', 'confirm', 'payment_status', 'order_date', 'order_price')
    list_filter = ('confirm', 'payment_status', )
    readonly_fields  = ('id', 'user_id')
    actions = [make_order_done, make_order_confirmed_by_admin, make_order_unconfirmed_by_user, make_order_pending, 'delete_selected']
    fieldsets_with_inlines = [
        ('Информация о клиенте', {
            'fields': [
                ('last_name'),('first_name'), ('fathers_name'), ('phone_number'), ('email')]}),
        OrderItemTable,
        ('Информация о заказе', {
            'fields': [
                ('order_price'), ('currency'), ('payment_status'), ('confirm'), ('order_date')]}),
        
        ('Адрес доставки', {
            'fields': [
                ('delivery_type'), ('payment_type'), ('city'), ('street'), ('house'), ('nova_pochta'), ('ukr_pochta')]}),
        
    ]
    inlines = [OrderItemTable]
    model = Orders

