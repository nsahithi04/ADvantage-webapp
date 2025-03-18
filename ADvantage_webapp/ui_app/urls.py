from django.urls import path
from . import views

urlpatterns = [
    path('ad_generator_frame/', views.ad_generator_frame, name='ad_generator_frame'),
    path('ad_generator_payment_frame/', views.ad_generator_payment_frame, name='ad_generator_payment_frame'),
]