"""
Main URL configuration for CyberSec Toolkit.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', include('django.contrib.auth.urls')),
    path('password/', include('password_checker.urls')),
    path('encryption/', include('encryption_tool.urls')),
    path('phishing/', include('phishing_sim.urls')),
    path('integrity/', include('file_integrity.urls')),
]

# Register URL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    from django.shortcuts import render
    return render(request, 'registration/register.html', {'form': form})

urlpatterns += [
    path('accounts/register/', register_view, name='register'),
]
