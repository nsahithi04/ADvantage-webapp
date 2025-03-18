from django.urls import path
from . import views

urlpatterns = [
    path('adgenframe1/', views.adgenframe1, name='adgenframe1'),
    path('adgenframe2/', views.adgenframe2, name='adgenframe2'),
]