# Generated by Django 3.2.4 on 2021-06-13 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210613_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='unit_weight',
            new_name='unit_weight_kg',
        ),
    ]
