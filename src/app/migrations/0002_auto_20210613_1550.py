# Generated by Django 3.2.4 on 2021-06-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='uuid',
        ),
        migrations.AddField(
            model_name='item',
            name='country_id',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer_id',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='number_id',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
