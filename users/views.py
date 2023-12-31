from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import AuditLog
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

# Create your views here.
@login_required
def userDetails(request):
    return render(request, 'userinfo.html')

# Overriding the default login class
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def form_valid(self, form):
        # Check if the login is valid and create an audit entry then save it to the db
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        audit_log = AuditLog.objects.create(
            date=date.today(),
            time=datetime.now().time(),
            username=username,
            activity_type='Login'
        )
        audit_log.save()

        return response
    

@login_required
# Custom logout function
def custom_logout(request):
    # Create an audit entry then save it to the db
    username = request.user.username
    audit_log = AuditLog.objects.create(
        date=date.today(),
        time=datetime.now().time(),
        username=username,
        activity_type='Logout'
    )
    audit_log.save()

    # Redirect to the login screen
    logout_view = LogoutView.as_view(next_page='login')
    return logout_view(request)

# Overriding the default change password class
class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        # Check if the login is valid and create an audit entry then save it to the db
        response = super().form_valid(form)
        username = self.request.user.username
        audit_log = AuditLog.objects.create(
            date=date.today(),
            time=datetime.now().time(),
            username=username,
            activity_type='Password Change'
        )
        audit_log.save()
        return response