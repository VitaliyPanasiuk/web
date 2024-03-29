from tkinter import CASCADE
from turtle import hideturtle
from django.db import models
from random import randint
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

#functions
def random_string():
    result = randint(100000000, 999999999)
    return result
    
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
CONFIRM_STATUS = (
    ('uc', 'В обработке'),
    ('unc', 'Заказ не подтвержден пользователем'),
    ('ac', 'Заказ подтвержден администратором'),
    ('done', 'Заказ выполнен'),
)
CURRENCIES = (
    ('USD', 'USD'),
    ('UAH', 'UAH'),
)
AMOUNT = (
    ('шт.', 'шт.'),
)

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)




class AuthUser(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, null=False,)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
    ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
    user_language = models.CharField(max_length=45, blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):          
        return f"{self.first_name} {self.last_name} "

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ShopCurrency(models.Model):
        date = models.DateTimeField(blank=True, null=True, verbose_name='Дата', default=datetime.datetime.now())
        usd_to_uah = models.IntegerField(verbose_name='Курс $ к ₴')

        class Meta:
            managed = False
            db_table = 'shop_currency'
            verbose_name_plural = "Курсы валют"
            verbose_name = "Курс валют"



class ShopCalls(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, null=False,)
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Номер телефона')
    timedate = models.DateTimeField(blank=True, null=True, verbose_name='Дата создания запроса')
    viewed_product = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Просматриваемый продукт")
    price = models.CharField(max_length=100, blank=True, null=True, verbose_name='Цена продукта')

    class Meta:
        db_table = 'shop_calls'
        verbose_name_plural = "Запросы звонков"
        verbose_name = "Запрос звонка"

    def __str__(self):
        return 'Запрос от номера ' + str(self.phone_number)

class ShopSubCategory(models.Model):
    subcategory_name_ru = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на русском')
    subcategory_name_en = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на английском')
    subcategory_name_uk = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на украинском')
    subcategory_id = models.CharField(max_length=500, blank=True, null=True, verbose_name='Id подкатегории')
    

    class Meta:
        verbose_name_plural = "Подкатегории"
        verbose_name = "Подкатегория"
        db_table = 'shop_subcategory'
    def __str__(self):
        #return self.subcategory_name_ru
        return self.subcategory_id


class ShopCategory(models.Model):
    category_name_ru = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на русском')
    category_name_en = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на английском')
    category_name_uk = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Название на украинском')
    подкатегория = models.ManyToManyField(ShopSubCategory)
    #category_id = models.CharField(max_length=300, blank=True, null=True, verbose_name='Id категории')

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        db_table = 'shop_category'
    def __str__(self):
        return self.category_name_ru
 
class Products(models.Model):
    название_позиции = models.CharField(db_column='Название_позиции', max_length=98, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='id', primary_key=True, null=False,)
    код_товара = models.CharField(db_column='Код_товара', max_length=25, blank=True, null=True)  # Field name made lowercase.
    название_позиции_укр = models.CharField(db_column='Название_позиции_укр', max_length=90, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название позиции англ')
    поисковые_запросы = models.CharField(db_column='Поисковые_запросы', max_length=171, blank=True, null=True)  # Field name made lowercase.
    поисковые_запросы_укр = models.CharField(db_column='Поисковые_запросы_укр', max_length=169, blank=True, null=True)  # Field name made lowercase.
    описание = models.TextField(db_column='Описание', max_length=5231, blank=True, null=True)  # Field name made lowercase.
    описание_укр = models.TextField(db_column='Описание_укр', max_length=6656, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(max_length=5000, blank=True, null=True)
    тип_товара = models.CharField(db_column='Тип_товара', max_length=1, blank=True, null=True)  # Field name made lowercase.
    цена = models.FloatField(db_column='Цена', blank=True, null=True)  # Field name made lowercase.
    валюта = models.CharField(db_column='Валюта', max_length=3, blank=True, null=True, choices=CURRENCIES)  # Field name made lowercase.
    единица_измерения = models.CharField(db_column='Единица_измерения', max_length=8, blank=True, null=True, choices=AMOUNT)  # Field name made lowercase.
    минимальный_объем_заказа = models.IntegerField(db_column='Минимальный_объем_заказа', blank=True, null=True)  # Field name made lowercase.
    оптовая_цена = models.DecimalField(db_column='Оптовая_цена', max_digits=11, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    минимальный_заказ_опт = models.IntegerField(db_column='Минимальный_заказ_опт', blank=True, null=True)  # Field name made lowercase.
    ссылка_изображения = models.CharField(db_column='Ссылка_изображения', max_length=828, blank=True, null=True)  # Field name made lowercase.
    наличие = models.CharField(db_column='Наличие', max_length=2, blank=True, null=True, default='np', choices=AVAILABLE_STATUS)  # Field name made lowercase.
    количество = models.IntegerField(db_column='Количество', blank=True, null=True)  # Field name made lowercase.
    номер_группы = models.IntegerField(db_column='Номер_группы', blank=True, null=True)  # Field name made lowercase.
    адрес_подраздела = models.CharField(db_column='Адрес_подраздела', max_length=77, blank=True, null=True)  # Field name made lowercase.
    возможность_поставки = models.IntegerField(db_column='Возможность_поставки', blank=True, null=True)  # Field name made lowercase.
    срок_поставки = models.CharField(db_column='Срок_поставки', max_length=7, blank=True, null=True)  # Field name made lowercase.
    способ_упаковки = models.CharField(db_column='Способ_упаковки', max_length=40, blank=True, null=True)  # Field name made lowercase.
    идентификатор_товара = models.CharField(db_column='Идентификатор_товара', max_length=24, blank=True, null=True)  # Field name made lowercase.
    идентификатор_подраздела = models.IntegerField(db_column='Идентификатор_подраздела', blank=True, null=True)  # Field name made lowercase.
    идентификатор_группы = models.CharField(db_column='Идентификатор_группы', max_length=30, blank=True, null=True)  # Field name made lowercase.
    производитель = models.CharField(db_column='Производитель', max_length=11, blank=True, null=True)  # Field name made lowercase.
    страна_производитель = models.CharField(db_column='Страна_производитель', max_length=11, blank=True, null=True)  # Field name made lowercase.
    скидка = models.IntegerField(db_column='Скидка', blank=False, null=False, verbose_name='Скидка (%)', default=0 ,validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])  # Field name made lowercase.
    id_группы_разновидностей = models.CharField(db_column='ID_группы_разновидностей', max_length=30, blank=True, null=True)  # Field name made lowercase.
    личные_заметки = models.CharField(db_column='Личные_заметки', max_length=30, blank=True, null=True)  # Field name made lowercase.
    image = models.FileField(upload_to='products/', blank=True, null=True, verbose_name='Главное изображение')
    category_name = models.CharField(db_column='category_name', max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'shop_product'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    def __str__(self):
        return self.название_позиции

class Image(models.Model):
    image = models.ImageField(upload_to='productInfo/', verbose_name='Изображение')
    product = models.ForeignKey(Products, default=None, related_name='images', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'    


class ShopCart(models.Model):
    user_id = models.CharField(max_length=45)
    item = models.CharField(max_length=45, blank=True, null=True)
    cart_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True, default=1)
    name = models.CharField(max_length=300, blank=True, null=True)
    price = models.CharField(max_length=30, blank=True, null=True)
    currency = models.CharField(max_length=30, blank=True, null=True)
    ru_order_item = models.CharField(max_length=500, null=True, blank=True)
    uk_order_item = models.CharField(max_length=500, null=True, blank=True)
    en_order_item = models.CharField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'shop_cart'
