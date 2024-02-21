from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

from .views import (
    ItemListView,
    ItemDetailView,
    AddToCartView,
    OrderDetailView,
    OrderQuantityUpdateView,
    OrderItemDeleteView,
    AddToCartNewView,
    IncreaseStockView,
    ConfirmOrderView,
    OrderViewSet,
    DeleteOrderItems,
    ConfirmPaymentOrderView,
    SearchView,
)


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet) 
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)
router.register('barcodes', views.BarcodeViewSet)
router.register('messages', views.MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('search/', SearchView.as_view(), name='search'),
    path('products-list/', ItemListView.as_view(), name='product-list'),
    path('product-details/<pk>/', ItemDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', AddToCartNewView.as_view(), name='add-to-cart'),
    path('add-stock/', IncreaseStockView.as_view(), name='add-stock'),
    path('order-summary/', OrderDetailView.as_view(), name='order-summary'),
    path('order-confirm/', ConfirmOrderView.as_view(), name='order-confirm'),
    path('order-confirm-payment/', ConfirmPaymentOrderView.as_view(), name='order-confirm-payment'),
    path('order-clear/', DeleteOrderItems.as_view(), name='order-clear'),
    path('order-items/<pk>/delete/',
         OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('order-item/update-quantity/',
         OrderQuantityUpdateView.as_view(), name='order-item-update-quantity'),
]