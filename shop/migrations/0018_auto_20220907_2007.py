# Generated by Django 3.2.15 on 2022-09-07 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20220907_2002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
