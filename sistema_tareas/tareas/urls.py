from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('signup', RegisterView.as_view(), name='register'),  # URL para el registro
    path('login', LoginView.as_view(), name='login'),          # URL para el login
]
