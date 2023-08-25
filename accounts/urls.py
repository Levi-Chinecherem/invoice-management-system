from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('custom-login/', views.custom_login, name='custom_login'),
    path('custom-signup/', views.custom_signup, name='custom_signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
