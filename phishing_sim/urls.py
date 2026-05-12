from django.urls import path
from . import views

app_name = 'phishing_sim'

urlpatterns = [
    path('', views.simulator_home, name='home'),
    path('scenario/<int:pk>/', views.scenario_view, name='scenario'),
    path('scenario/<int:pk>/submit/', views.submit_answers, name='submit'),
    path('progress/', views.progress_view, name='progress'),
]
