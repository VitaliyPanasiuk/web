# Generated by Django 3.2.15 on 2022-09-06 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_usercart_usercartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCart',
        ),
        migrations.DeleteModel(
            name='UserCartItem',
        ),
    ]
