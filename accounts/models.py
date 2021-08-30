from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

PROGRESS_STATUS = (
    ('d', 'Исполнено'),
    ('nd', 'Не исполнено'),
)
PAYMENT_STATUS = (
    ('p', 'Оплачено'),
    ('np', 'Не оплачено'),
)
AVAILABLE_STATUS = (
    ('a', 'Есть в наличии'),
    ('ua', 'Нет в наличии'),
)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=254)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
    ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'auth_user'

class Продукт(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, null=False,)
    код_товара = models.CharField(db_column='Код_товара', max_length=25, blank=True, null=True)  # Field name made lowercase.
    название_позиции = models.CharField(db_column='Название_позиции', max_length=98, blank=True, null=True)  # Field name made lowercase.
    название_позиции_укр = models.CharField(db_column='Название_позиции_укр', max_length=90, blank=True, null=True)  # Field name made lowercase.
    поисковые_запросы = models.CharField(db_column='Поисковые_запросы', max_length=171, blank=True, null=True)  # Field name made lowercase.
    поисковые_запросы_укр = models.CharField(db_column='Поисковые_запросы_укр', max_length=169, blank=True, null=True)  # Field name made lowercase.
    описание = models.CharField(db_column='Описание', max_length=5231, blank=True, null=True)  # Field name made lowercase.
    описание_укр = models.CharField(db_column='Описание_укр', max_length=6656, blank=True, null=True)  # Field name made lowercase.
    тип_товара = models.CharField(db_column='Тип_товара', max_length=1, blank=True, null=True)  # Field name made lowercase.
    цена = models.IntegerField(db_column='Цена', blank=True, null=True)  # Field name made lowercase.
    валюта = models.CharField(db_column='Валюта', max_length=3, blank=True, null=True)  # Field name made lowercase.
    единица_измерения = models.CharField(db_column='Единица_измерения', max_length=8, blank=True, null=True)  # Field name made lowercase.
    минимальный_объем_заказа = models.DecimalField(db_column='Минимальный_объем_заказа', max_digits=5, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    оптовая_цена = models.DecimalField(db_column='Оптовая_цена', max_digits=11, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    минимальный_заказ_опт = models.DecimalField(db_column='Минимальный_заказ_опт', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ссылка_изображения = models.CharField(db_column='Ссылка_изображения', max_length=828, blank=True, null=True)  # Field name made lowercase.
    наличие = models.CharField(db_column='Наличие', max_length=2, blank=True, null=True, default='np', choices=AVAILABLE_STATUS)  # Field name made lowercase.
    количество = models.IntegerField(db_column='Количество', blank=True, null=True)  # Field name made lowercase.
    номер_группы = models.IntegerField(db_column='Номер_группы', blank=True, null=True)  # Field name made lowercase.
    название_группы = models.CharField(db_column='Название_группы', max_length=100, blank=True, null=True)  # Field name made lowercase.
    адрес_подраздела = models.CharField(db_column='Адрес_подраздела', max_length=77, blank=True, null=True)  # Field name made lowercase.
    возможность_поставки = models.IntegerField(db_column='Возможность_поставки', blank=True, null=True)  # Field name made lowercase.
    срок_поставки = models.CharField(db_column='Срок_поставки', max_length=7, blank=True, null=True)  # Field name made lowercase.
    способ_упаковки = models.CharField(db_column='Способ_упаковки', max_length=40, blank=True, null=True)  # Field name made lowercase.
    идентификатор_товара = models.CharField(db_column='Идентификатор_товара', max_length=24, blank=True, null=True)  # Field name made lowercase.
    идентификатор_подраздела = models.IntegerField(db_column='Идентификатор_подраздела', blank=True, null=True)  # Field name made lowercase.
    идентификатор_группы = models.CharField(db_column='Идентификатор_группы', max_length=30, blank=True, null=True)  # Field name made lowercase.
    производитель = models.CharField(db_column='Производитель', max_length=11, blank=True, null=True)  # Field name made lowercase.
    страна_производитель = models.CharField(db_column='Страна_производитель', max_length=11, blank=True, null=True)  # Field name made lowercase.
    скидка = models.CharField(db_column='Скидка', max_length=30, blank=True, null=True)  # Field name made lowercase.
    id_группы_разновидностей = models.CharField(db_column='ID_группы_разновидностей', max_length=30, blank=True, null=True)  # Field name made lowercase.
    личные_заметки = models.CharField(db_column='Личные_заметки', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cрок_действия_скидки_от = models.CharField(db_column='Cрок_действия_скидки_от', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cрок_действия_скидки_до = models.CharField(db_column='Cрок_действия_скидки_до', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_product'
        verbose_name_plural = "Продукты"
    

class ShopCart(models.Model):
    user_id = models.CharField(max_length=45)
    item = models.CharField(max_length=90, blank=True, null=True)
    cart_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True, default=1)
    name = models.CharField(max_length=300, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    currency = models.CharField(max_length=30, blank=True, null=True)
    admin_order_item = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'shop_cart'

class ShopCurrency(models.Model):
        date = models.DateTimeField(blank=True, null=True)
        usd_to_uah = models.CharField(max_length=100)

        class Meta:
            managed = False
            db_table = 'shop_currency'

class Заказ(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, null=False,)
    фамилия = models.CharField(max_length=45)
    имя = models.CharField(max_length=45)
    отчество = models.CharField(max_length=45, blank=True, null=True)
    телефон = models.CharField(max_length=45, blank=True, null=True)
    почта = models.CharField(max_length=60)
    заказ = models.TextField(max_length=10000, blank=True, null=True)
    user_order = models.CharField(max_length=10000, blank=True, null=True)
    сумма_заказа = models.CharField(max_length=45, blank=True, null=True)
    валюта_заказа = models.CharField(max_length=45, blank=True, null=True)
    статус_оплаты = models.CharField(max_length=45, blank=True, null=False, default='np', choices=PAYMENT_STATUS)
    статус_заказа = models.CharField(max_length=45, blank=True, null=False, default='nd', choices=PROGRESS_STATUS, verbose_name='Статус Заказа')
    дата_заказа = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Id пользователя')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name='Улица')
    house = models.CharField(max_length=50, blank=True, null=True, verbose_name='Дом')
    payment_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='Тип оплаты')
    delivery_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='Тип доставки')
    nova_pochta = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Отделение Новой Почты')
    ukr_pochta = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Индекс почтового отеделния')
    confirm = models.CharField(max_length=500, blank=True, null=True)
    raworder = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')

    class Meta:
        managed = False
        db_table = 'shop_order'
        verbose_name_plural = 'Заказы'
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    def __str__(self):
        return 'Заказ №' + str(self.id)