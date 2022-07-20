from django.urls import path
from .views import coffee_obj, get_coffee
from . import views

urlpatterns = [
    path('coffee_obj/', views.coffee_obj ),
    path('get_coffee/<int:pk>', views.get_coffee),
    path('get_coffee/', views.get_coffee),
    path('update_coffee/<int:pk>', views.update_coffee)
]
