"""sdndefender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', custom_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('audits/', include('audits.urls')),
    path('pefiles/', include('pefiles.urls')),
    path('notification/', include('notification.urls')),
    path('information/', include('information.urls')),
]
