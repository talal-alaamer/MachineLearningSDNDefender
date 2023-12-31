from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def showPrivacy(request):
    return render(request, 'privacy.html')

@login_required
def showTerms(request):
    return render(request, 'terms.html')