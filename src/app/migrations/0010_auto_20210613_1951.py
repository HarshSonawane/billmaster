# Generated by Django 3.2.4 on 2021-06-13 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210613_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='barcoded_manual',
        ),
        migrations.RemoveField(
            model_name='item',
            name='manual_uid',
        ),
    ]