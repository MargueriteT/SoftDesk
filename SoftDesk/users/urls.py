from django.urls import path
from .views import UserRegisterAPIView

urlpatterns = [
    path('signup/', UserRegisterAPIView.as_view(), name='register')]