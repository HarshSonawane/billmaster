from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import (
    Order, OrderItem, Item, Address, Category, Barcode, Message
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'parrent', 'image', 'title', 'is_active')


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ('pk', 'user', 'image')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'title', 'text')


class ItemSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()
    type_title = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'user',
            'category',
            'category_title',
            'price',
            'stock',
            'capacity',
            'type',
            'type_title',
            'uid',
            'barcode',
            'is_temprory',
        )

    def get_category_title(self, obj):
        return obj.category.title if obj.category else None

    def get_type_title(self, obj):
        return obj.get_type_display()



class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'item',
            'quantity',
            'final_price'
        )

    def get_item(self, obj):
        return ItemSerializer(obj.item).data

    def get_final_price(self, obj):
        return obj.get_total_item_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'date',
            'user',
            'customer_name',
            'customer_mobile',
            'ordered_date',
            'status',
            'order_items',
            'is_payment_done',
            'ordered',
            'total',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_date(self, obj):
        return obj.ordered_date.date()


class ItemDetailSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'user',
            'category',
            'stock',
            'category_title',
            'price',
            'capacity',
            'stock',
            'type',
            'description',
            'image',
            'is_temprory'
        )

    def get_category_title(self, obj):
        return obj.category.title if obj.category else None

    def get_type_title(self, obj):
        return obj.get_type_display()