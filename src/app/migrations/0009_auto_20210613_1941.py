# Generated by Django 3.2.4 on 2021-06-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_item_barcoded_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='manual_uid',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='item',
            name='uid',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
