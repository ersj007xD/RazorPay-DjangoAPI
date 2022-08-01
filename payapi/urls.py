from django.urls import path
from payapi.views import coffee_obj, get_coffee, UserRegistrationView, UserLoginView, User_view, UserChangePassword
from . import views

urlpatterns = [
    path('coffee_obj/', views.coffee_obj ),
    path('get_coffee/<int:pk>', views.get_coffee),
    path('get_coffee/', views.get_coffee),
    path('update_coffee/<int:pk>', views.update_coffee),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user_details/<str:name>', views.User_view),
    path('change_password/', UserChangePassword.as_view()),
]
