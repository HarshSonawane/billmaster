# Generated by Django 3.2.5 on 2021-08-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20210728_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Placed'), (2, 'Shipped'), (3, 'Completed'), (4, 'Canceled/Refunded')], default=1, null=True),
        ),
    ]