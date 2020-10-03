from django.urls import path
from . import views

urlpatterns = [
    path('webhook_listener_with_response/', views.webhook_listener_with_response),
]
