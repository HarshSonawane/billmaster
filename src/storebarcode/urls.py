from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_auth.views import PasswordResetConfirmView
from app.views import GoogleLogin, FacebookLogin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('app.urls')),
    path('rest/auth/', include('rest_auth.urls')),
    path('rest/auth/google/', GoogleLogin.as_view()),
    path('rest/auth/facebook/', FacebookLogin.as_view()),
    path('rest/auth/register/', include('rest_auth.registration.urls')),
    path('rest/auth/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)