from django.urls import path
from . import views

app_name = 'encryption_tool'

urlpatterns = [
    path('', views.tool_view, name='tool'),
    path('encrypt/', views.encrypt_view, name='encrypt'),
    path('decrypt/', views.decrypt_view, name='decrypt'),
]
