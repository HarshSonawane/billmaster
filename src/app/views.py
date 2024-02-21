from django.shortcuts import render
from . import serializers
from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Category, Item, Address

from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

import requests
import json
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import (
    ItemSerializer, OrderSerializer, ItemDetailSerializer,
)
from .models import Item, OrderItem, Order, Address, Barcode, Message

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from google.oauth2 import id_token
from google.auth.transport import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from allauth.socialaccount.providers.google.provider import GoogleProvider
from .service import verify_token, manual_login


class GoogleOAuth2AdapterIdToken(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        idinfo = id_token.verify_oauth2_token(token.token, requests.Request(), app.client_id)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        extra_data = idinfo
        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2AdapterIdToken)
oauth2_callback = OAuth2CallbackView.adapter_view(GoogleOAuth2AdapterIdToken)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2AdapterIdToken
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class FacebookLogin(APIView):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('code', None)
        token = request.POST.get('access_token', None)

        if id is None or token is None:
            return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)

        result = verify_token(id, token)        

        if result["status"] is False:
            return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)
        else:
            if result["data"]["id"] is None:
                return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = User.objects.get(username=id)
                except User.DoesNotExist:
                    first_name, last_name = result["data"]["name"].split(" ")[0], result["data"]["name"].split(" ")[1]
                    user = User.objects.create(username=id, first_name=first_name, last_name=last_name)
                    user.set_password(id)
                    user.save()

                result = manual_login(user)
            
                try:
                    if result["key"] is not None:
                        return Response({"message": "Login successful", "key": result["key"]}, status=HTTP_200_OK)
                    else:
                        return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)
                except KeyError:
                    return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)
                    

        return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('-created')
    serializer_class = serializers.CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            request.data["added_by"] = self.kwargs.get("user") if self.kwargs.get("user") else request.user.id
        else:
            request.data["added_by"] = request.user.id

        return super().create(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            request.data["user"] = self.kwargs.get("user") if self.kwargs.get("user") else request.user.id
        else:
            request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_temprory=False).order_by('-created')
    serializer_class = serializers.ItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'


    def get_queryset(self):
        queryset = Item.objects.filter(is_temprory=False, user=self.request.user).order_by('-created')
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            request.data["user"] = self.kwargs.get("user") if self.kwargs.get("user") else request.user.id
        else:
            request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter().order_by('-pk')
    serializer_class = serializers.OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            request.data["user"] = self.kwargs.get("user") if self.kwargs.get("user") else request.user.id
        else:
            request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.filter(ordered=True)
    serializer_class = serializers.OrderItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            request.data["user"] = self.kwargs.get("user") if self.kwargs.get("user") else request.user.id
        else:
            request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)


class ItemListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemDetailSerializer
    queryset = Item.objects.all()


class BarcodeViewSet(viewsets.ModelViewSet):
    queryset = Barcode.objects.all()
    serializer_class = serializers.BarcodeSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'


class OrderQuantityUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid', None)
        if uid is None:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item, uid=uid)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__uid=item.uid).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                return Response(status=HTTP_200_OK)
            else:
                return Response({"message": "This item was not in your cart"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)


class OrderItemDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = OrderItem.objects.all()


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.POST.get('uid', None)
        variations = request.POST.get('variations', [])
        if uid is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, uid=uid)

        minimum_variation_count = Variation.objects.filter(item=item).count()
        if len(variations) < minimum_variation_count:
            return Response({"message": "Please specify the required variation types"}, status=HTTP_400_BAD_REQUEST)

        order_item_qs = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )
        for v in variations:
            order_item_qs = order_item_qs.filter(
                Q(item_variations__exact=v)
            )

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                item=item,
                user=request.user,
                ordered=False
            )
            order_item.item_variations.add(*variations)
            order_item.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.items.filter(item__id=order_item.id).exists():
                order.items.add(order_item)
                return Response(status=HTTP_200_OK)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return Response(status=HTTP_200_OK)


class AddToCartNewView(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.POST.get('uid', None)
        item = get_object_or_404(Item, uid=uid, user=request.user)
        quanntity = int(request.POST.get('quantity', 1))

        if item.stock < quanntity:
            return Response({"message": "Stock is less than quantity"}, status=HTTP_400_BAD_REQUEST)

        # try:
        #     order_item = OrderItem.objects.get(user=request.user, ordered=False, item=item)
        # except OrderItem.DoesNotExist:
        #     order_item = OrderItem.objects.create(
        #         item=item,
        #         user=request.user,
        #         ordered=False)

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__uid=item.uid).exists():
                order_item.quantity += quanntity
                if item.stock < quanntity:
                    return Response({"message": "Stock is less than quantity"}, status=HTTP_400_BAD_REQUEST)
                order_item.save()
                item.stock -= quanntity
                item.save()
                return Response({"message": "This item quantity was updated.", "Quantity": order_item.quantity}, status=HTTP_200_OK)
            else:
                order.items.add(order_item)
                if item.stock < quanntity:
                    return Response({"message": "Stock is less than quantity"}, status=HTTP_400_BAD_REQUEST)
                item.stock -= quanntity
                item.save()
                return Response({"message": "This item was added to your cart.", "Quantity": quanntity}, status=HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date, ordered=False)
            order.items.add(order_item)
            if item.stock < quanntity:
                return Response({"message": "Stock is less than quantity"}, status=HTTP_400_BAD_REQUEST)
            item.stock -= quanntity
            item.save()
            return Response({"message": "This item was added to your cart.", "Quantity": quanntity}, status=HTTP_200_OK)


class IncreaseStockView(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.POST.get('uid', None)
        quanntity = int(request.POST.get('quantity', 1))

        try:
            item = Item.objects.get(uid=uid)
            item.stock += quanntity
            item.save()
            return Response({"message": "Stock was updated", "Quantity": item.stock}, status=HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"message": "Item not found."}, status=HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    def post(self, request, *args, **kwargs):
        q = request.POST.get('q', None)
        if q.isdigit():
            return Response({"data": OrderSerializer(Order.objects.filter(Q(pk=q ) | Q(customer_mobile__icontains=q)), many=True).data}, status=HTTP_200_OK)
        return Response({"data": OrderSerializer(Order.objects.filter(Q(customer_name__icontains=q) | Q(customer_mobile__icontains=q)), many=True).data}, status=HTTP_200_OK)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")


class ConfirmOrderView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        try:
            order = Order.objects.get(pk=id)
            order.status = 3
            order.ordered = True
            order.save()
            for item in order.items.all():
                item.ordered = True
                item.save()
            return Response({"message": "Your order was confirmed"}, status=HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)


class ConfirmPaymentOrderView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        try:
            order = Order.objects.get(pk=id)
            order.status = 3
            order.ordered = True
            order.is_payment_done = True
            order.save()
            for item in order.items.all():
                item.ordered = True
                item.save()
            return Response({"message": "Your order was confirmed"}, status=HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"message": "Something went wrong."}, status=HTTP_400_BAD_REQUEST)


class DeleteOrderItems(APIView):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        try:
            order = Order.objects.get(pk=id, ordered=False)
            for item in order.items.all():
                item.delete()
            return Response({"message": "All items were deleted"}, status=HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"message": "Order is already confirmed or Something else went wrong."}, status=HTTP_400_BAD_REQUEST)
