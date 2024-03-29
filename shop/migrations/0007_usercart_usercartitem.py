# Generated by Django 3.2.15 on 2022-09-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_orderitem_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCartItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_id', models.IntegerField()),
                ('name_uk', models.CharField(blank=True, max_length=200, null=True)),
                ('name_en', models.CharField(blank=True, max_length=200, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=45, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('cart_items', models.ManyToManyField(to='shop.UserCartItem')),
            ],
        ),
    ]
