from django.urls import path
from . import views
from django.conf.urls import include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'req-doc', views.RequirementsDocView)
router.register(r'quote', views.VendorQuotesView)

urlpatterns = [
    url('', include(router.urls)),
    path('req-doc/<int:pk>/final-list/', views.FinalList.as_view(), name= 'final-list'),
    path('req-doc/<int:pk>/items/', views.ItemsAPI.as_view(), name= 'items-api'),
    path('req-doc/<int:pk>/quotes/', views.ClientQuotesView.as_view(), name= 'quotes-api'),
    #path('req-doc/<int:pk>/quote', views.VendorQuotesView)
]