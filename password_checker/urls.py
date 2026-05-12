from django.urls import path
from . import views

app_name = 'password_checker'

urlpatterns = [
    path('', views.checker_view, name='checker'),
    path('check/', views.check_password_ajax, name='check_ajax'),
]
