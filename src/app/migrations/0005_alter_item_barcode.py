# Generated by Django 3.2.4 on 2021-06-13 16:49

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210613_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.ImageField(blank=True, upload_to=app.models.upload_file_path),
        ),
    ]
