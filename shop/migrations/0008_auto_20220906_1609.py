# Generated by Django 3.2.15 on 2022-09-06 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_usercart_usercartitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercart',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='usercartitem',
            options={'managed': False},
        ),
    ]
