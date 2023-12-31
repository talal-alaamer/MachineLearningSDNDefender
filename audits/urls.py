from django.urls import path
from audits import views

app_name='audits'
urlpatterns = [
    path('', views.viewAudits, name="viewaudits"),
]