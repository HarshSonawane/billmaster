# Generated by Django 3.2.4 on 2021-06-13 15:33

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.CharField(max_length=400)),
                ('line_2', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=6)),
                ('country', models.CharField(default='India', max_length=100)),
                ('type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Other'), (1, 'Home'), (2, 'Office')], null=True)),
                ('latitude', models.CharField(max_length=30)),
                ('logitude', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to=app.models.upload_file_path)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('parrent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=20)),
                ('image', models.ImageField(upload_to=app.models.upload_file_path)),
                ('barcode', models.ImageField(blank=True, upload_to=app.models.barcode_upload_file_path)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('buying_price', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Placed'), (3, 'Shipped'), (4, 'Completed'), (5, 'Canceled/Refunded')], default=1, null=True)),
                ('received', models.BooleanField(default=False)),
                ('ordered', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='app.OrderItem')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='app.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]