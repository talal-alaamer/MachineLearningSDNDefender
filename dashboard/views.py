from django.shortcuts import render
from matplotlib.dates import relativedelta
from pefiles.models import PeFile
from .models import CaptureLog
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date as dt
import requests
import json
from django.utils.timezone import make_aware

# Create your views here.
@login_required
def detectionDashboard(request):
    # Load all detection records
    allFiles = PeFile.objects.all()

    # Create variables for the dashboard stats and visuals
    malwareCount = allFiles.filter(Type="Malware").count()
    benignCount = allFiles.filter(Type="Benign").count()
    allCount = allFiles.count()
    date = datetime.now()
    todayCount = allFiles.filter(Date=date).count()
    benignPercentage = benignCount/allCount
    malwarePercentage = malwareCount/allCount
    last7Days = {
        'today':{
            'Date': date.strftime("%b %d"),
            'Benign': allFiles.filter(Date=date, Type="Benign").count(),
            'Malware': allFiles.filter(Date=date, Type="Malware").count(),
        },
        'beforeOneDay':{
            'Date': (date - timedelta(days=1)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=1), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=1), Type="Malware").count(),
        },
        'beforeTwoDays':{
            'Date': (date - timedelta(days=2)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=2), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=2), Type="Malware").count(),
        },
        'beforeThreeDays':{
            'Date': (date - timedelta(days=3)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=3), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=3), Type="Malware").count(),
        },
        'beforeFourDays':{
            'Date': (date - timedelta(days=4)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=4), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=4), Type="Malware").count(),
        },
        'beforeFiveDays':{
            'Date': (date - timedelta(days=5)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=5), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=5), Type="Malware").count(),
        },
        'beforeSixDays':{
            'Date': (date - timedelta(days=6)).strftime("%b %d"),
            'Benign': allFiles.filter(Date=date - timedelta(days=6), Type="Benign").count(),
            'Malware': allFiles.filter(Date=date - timedelta(days=6), Type="Malware").count(),
        },
    }

    today = dt.today()
    endDate = datetime.combine(today, datetime.min.time())
    startDate = dt(today.year, today.month, 1)
    oneMonthAgoEndDate = startDate - timedelta(days=1)
    oneMonthAgoStartDate = dt(oneMonthAgoEndDate.year, oneMonthAgoEndDate.month, 1)
    twoMonthsAgoEndDate = oneMonthAgoStartDate - timedelta(days=1)
    twoMonthsAgoStartDate = dt(twoMonthsAgoEndDate.year, twoMonthsAgoEndDate.month, 1)
    last3Months = {
        'thisMonth': {
            'Month': date.strftime('%B'),
            'Count': allFiles.filter(Date__gte=startDate, Date__lte=endDate, Type="Malware").count()
        },
        'oneMonthAgo': {
            'Month': (date - relativedelta(months=1)).strftime('%B'),
            'Count': allFiles.filter(Date__gte=oneMonthAgoStartDate, Date__lte=oneMonthAgoEndDate, Type="Malware").count(),
        },
        'twoMonthsAgo': {
            'Month': (date - relativedelta(months=2)).strftime('%B'),
            'Count': allFiles.filter(Date__gte=twoMonthsAgoStartDate, Date__lte=twoMonthsAgoStartDate, Type="Malware").count(),
        },
    }
    
    # Verify if the capturing script is running by comparing the current time with the runtime
    currentTime = datetime.now()
    scriptStatus = CaptureLog.objects.latest('timestamp')
    currentTimeAware = make_aware(currentTime)

    timeDifference = currentTimeAware - scriptStatus.timestamp
    withinTime = timeDifference <= timedelta(minutes=1)

    # Change the status indicator accordingly
    if withinTime:
        status = "Running"
    else:
        status = "Stopped"

    # Create a context dictionary to display all the info to the HTML page
    context = {
        'allCount': allCount,
        'benignCount': benignCount,
        'malwareCount': malwareCount,
        'todayCount': todayCount,
        'benignPercentage': benignPercentage,
        'malwarePercentage': malwarePercentage,
        'last7Days': last7Days,
        'last3Months': last3Months,
        'status': status,
    }

    return render(request, 'dashboards/detectiondashboard.html', context)

@login_required
def sdnanalytics(request):
    # Retrieve the network devices from the SDN controller and parse them
    response = get(api='network-device').json()
    data = response["response"]
    # Create a context dictionary to display all the info to the HTML page
    context = {
        "data": data,
    }
    return render(request, 'dashboards/sdnanalytics.html', context)

# Function to retrieve the session token to access the SDN controller API
def get_X_auth_token(ip="10.31.40.191",ver="v1",uname="admin",pword="Admin123@"):
    requests.packages.urllib3.disable_warnings()
    r_json = {
    "username": uname,
    "password": pword
    }
    post_url = "https://"+ip+"/api/"+ver+"/ticket"
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post(post_url, data = json.dumps(r_json), headers=headers,verify=False)
        return r.json()["response"]["serviceTicket"]
    except:
        print ("Status: %s"%r.status_code)
        print ("Response: %s"%r.text)

# Function to call the GET APIs of the SDN controller by specifing the API as argument
def get(ip="10.31.40.191",ver="v1",uname="admin",pword="Admin123@",api='',params=''):
    ticket = get_X_auth_token(ip,ver,uname,pword)
    headers = {"X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    try:
        resp= requests.get(url,headers=headers,params=params,verify = False)
        return(resp)
    except:
       print ("Something wrong with GET /",api)