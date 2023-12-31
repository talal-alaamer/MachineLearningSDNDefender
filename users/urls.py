from django.urls import path
from django.contrib.auth import views as auth_views
from users import views
from .views import CustomLoginView, CustomPasswordChangeView

app_name='users'
urlpatterns = [
    path('userdetails', views.userDetails, name="userdetails"),
    path('password_change/', CustomPasswordChangeView.as_view(template_name='password_change.html', success_url='/users/password_change_success'), name='password_change'),
    path('password_change_success/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_success.html'), name='password_change_success'),
]