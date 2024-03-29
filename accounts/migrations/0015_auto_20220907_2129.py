# Generated by Django 3.2.15 on 2022-09-07 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_orders_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='валюта_заказа',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='дата_заказа',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='заказ',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='имя',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='отчество',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='почта',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='статус_заказа',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='статус_оплаты',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='сумма_заказа',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='телефон',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='фамилия',
        ),
        migrations.AddField(
            model_name='orders',
            name='currency',
            field=models.CharField(blank=True, db_column='валюта_заказа', max_length=45, null=True, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='orders',
            name='email',
            field=models.CharField(blank=True, db_column='почта', max_length=60, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='orders',
            name='fathers_name',
            field=models.CharField(blank=True, db_column='отчество', max_length=45, null=True, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='orders',
            name='first_name',
            field=models.CharField(blank=True, db_column='имя', max_length=45, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='orders',
            name='last_name',
            field=models.CharField(blank=True, db_column='фамилия', max_length=45, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order',
            field=models.TextField(blank=True, db_column='заказ', max_length=10000, null=True, verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(blank=True, db_column='дата_заказа', null=True, verbose_name='Дата и время заказа'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_price',
            field=models.CharField(blank=True, db_column='сумма_заказа', max_length=45, null=True, verbose_name='Сумма заказа'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_status',
            field=models.CharField(blank=True, choices=[('d', 'Исполнено'), ('nd', 'Не исполнено')], db_column='статус_заказа', default='nd', max_length=45, verbose_name='Статус выполнения'),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('p', 'Оплачено'), ('np', 'Не оплачено')], db_column='статус_оплаты', default='np', max_length=45, verbose_name='Статус оплаты'),
        ),
        migrations.AddField(
            model_name='orders',
            name='phone_number',
            field=models.CharField(blank=True, db_column='телефон', max_length=45, null=True, verbose_name='Номер телефона'),
        ),
    ]
