from django.urls import path
from pefiles import views

app_name='PeFiles'
urlpatterns = [
    path('', views.displayPeFiles, name="displayPeFiles"),
    path('pefiles/details/<str:hash>/', views.showDetails, name='showDetails'),
    path('pefiles/details/<str:hash>/export/', views.export, name='export'),
]