from django.urls import path
from information import views

app_name='information'
urlpatterns = [
    path('privacy', views.showPrivacy, name="privacy"),
    path('terms', views.showTerms, name="terms"),
]