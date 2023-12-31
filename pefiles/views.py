from django.shortcuts import render
from django.urls import reverse
from .models import PeFile
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse

# Create your views here.

@login_required
def displayPeFiles(request):
    # Check if sorting is applied through the GET request
    if request.GET:
        column = request.GET.get('column', 'date')
        sort = request.GET.get('sort', 'desc')

        column_mapping = {
            'hash': '-sha256',
            'date': '-Date',
            'time': '-Time',
            'type': '-Type',
        }

        # Check the sort field and apply the sorting
        field_name = column_mapping.get(column, 'Date')
        pefiles = PeFile.objects.order_by(field_name)

        # Reverse the order of the files
        if sort == 'asc':
            pefiles = pefiles.reverse()

        # Filter results by file type selected
        file_type = request.GET.get('file_type')
        if file_type:
            pefiles = pefiles.filter(Type=file_type)

        # Filter results by search keyword
        search_query = request.GET.get('search')
        if search_query:
            pefiles = pefiles.filter(sha256__icontains=search_query)

        # Create a context dictionary to display all the info to the HTML page
        context = {
            'pefiles': pefiles,
            'sort': sort,
            'column': column,
            'file_type': file_type,
            'search_query': search_query,
        }

        return render(request, 'pefilelist.html', context)
    else:
        # Return all detection records from most recent to oldest
        pefiles = PeFile.objects.order_by('-Date', '-Time')
        return render(request, 'pefilelist.html', {'pefiles': pefiles})
    
@login_required
def showDetails(request, hash):
    # Retrieve the file details of the selected file
    pefile = PeFile.objects.order_by('-Date', '-Time').filter(sha256=hash).first()
    # Reverse for the export link and pass it to the context dictionary
    export_url = reverse('PeFiles:export', args=[hash])
    return render(request, 'pefiledetails.html', {'pefile': pefile, 'export_url': export_url})

# Function to export the file details to CSV
def export(request, hash):
    pefile = PeFile.objects.order_by('-Date', '-Time').filter(sha256=hash).first()

    # Create the http response object for the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{hash}.csv"'

    # Write the content of the CSV file and return the response
    writer = csv.writer(response)
    writer.writerow(['Field', 'Value'])

    for field in PeFile._meta.fields:
        field_name = field.name
        field_value = getattr(pefile, field_name, '')
        if(field_name!="id"):
            writer.writerow([field_name, field_value])

    return response