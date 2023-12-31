from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Notification

# Create your views here.
@login_required
def showNotifications(request):
    # Retrieve all the notifications and order them from latest to oldest
    audits = Notification.objects.order_by('-date', '-time')
    # Implement pagination displaying only 10 results per page
    paginator = Paginator(audits, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return the context dictionary to display the data to the HTML page
    return render(request, 'viewNotifications.html', {'page_obj': page_obj})
