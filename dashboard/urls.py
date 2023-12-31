from django.urls import path
from dashboard import views

app_name='dashboard'
urlpatterns = [
    path('', views.detectionDashboard, name="detectionDashboard"),
    path('sdnanalytics', views.sdnanalytics, name="sdnanalytics"),
]