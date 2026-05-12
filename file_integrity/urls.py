from django.urls import path
from . import views

app_name = 'file_integrity'

urlpatterns = [
    path('', views.checker_view, name='checker'),
    path('check/', views.check_file, name='check_file'),
]
