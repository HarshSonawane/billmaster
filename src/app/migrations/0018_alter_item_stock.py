# Generated by Django 3.2.4 on 2021-07-21 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_item_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
