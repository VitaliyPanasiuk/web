# Generated by Django 3.2.6 on 2021-08-30 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210830_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='продукт',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
