from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'notification'

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='notification/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]