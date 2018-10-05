from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path(r'payment_feedback/', views.receive_payment_feedback, name='payment_feedback'),
]
