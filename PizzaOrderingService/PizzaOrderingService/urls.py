
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from market.views import Menu
from service.views import OrderHandler


router = routers.DefaultRouter()
router.register(r'menu', Menu)
router.register(r'orders', OrderHandler, basename='')
router.register(r'orders/<pk>', OrderHandler, basename='')
router.register(r'orders/<pk>/status', OrderHandler, basename='')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
