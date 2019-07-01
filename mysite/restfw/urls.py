from django.contrib import admin
from django.urls import path, include
from .views import login, LoginView, UserViewset, InstagramView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewset)

urlpatterns = [
    path('login/', login, name='login'),
    path('', include(router.urls)),
    path('instagram/', InstagramView.as_view(), name='instagram'),
]
