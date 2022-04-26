"""picpassword URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('login/', views.login, name='login'),
    path('profile/<username>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('emailconfirmation/', views.emailconfirmation, name='emailconfirmation'),
    path('accountdeletionrequest/',views.accountdeletionrequest, name='accountdeletionrequest'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetpasswordotp/', views.resetpasswordotp, name='resetpasswordotp'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('changeusername/', views.changeusername, name='changeusername'),
]