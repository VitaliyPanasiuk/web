# Generated by Django 4.0.1 on 2022-06-24 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_shopcart_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='продукт',
            name='category_name',
            field=models.CharField(blank=True, db_column='category_name', max_length=30, null=True),
        ),
    ]
