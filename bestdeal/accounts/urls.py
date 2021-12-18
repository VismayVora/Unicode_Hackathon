from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('client_register/', views.ClientRegisterAPI.as_view(), name = 'Cient Registration'),
    path('vendor_register/', views.VendorRegisterAPI.as_view(), name = 'Vendor Registration'),
    path('login/', views.LoginAPI.as_view(), name = 'login'),
    path('email-verify/', views.EmailVerify.as_view(), name = 'email-verify'),
]