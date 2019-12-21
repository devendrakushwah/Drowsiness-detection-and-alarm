from django.http import *
import subprocess as sb, psutil as ps
import os
import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
import pytz
from .models import UserAnalytics

@login_required
def start(request):
    try:
        name = 'python'
        processes_ids = []
        for process in ps.process_iter():
            if process.name() == name:
                processes_ids.append(str(process.pid))
        if len(processes_ids) == 0:
            sb.Popen('./job.sh')
            time.sleep(4)

            for process in ps.process_iter():
                if process.name() == name:
                    processes_ids.append(str(process.pid))

            with open('process_id.txt', 'w') as f:
                f.write(','.join(processes_ids))
            f.close()

            # Code to save session start time
            with open('session_start.txt', 'w') as f:
                now = datetime.datetime.now()
                tz = pytz.timezone('Asia/Kolkata')
                now = now.astimezone(tz)
                date_string = now.strftime("%d/%m/%Y %H:%M:%S")
                f.write(date_string)
            f.close()

            #to initialise drowsiness count by 0
            with open('drowsiness_count.txt', 'w') as f:
                f.write('0')
            f.close()

            return render(request,'app/service_started.html',{})

    except Exception as e:
        print(e)

    return render(request,'app/service_started.html',{})

@login_required
def kill(request):
    try:
        with open('process_id.txt','r') as f:
            process_ids = f.readline().split(',')
        for i in process_ids:
            os.system('kill ' + i)

        now = datetime.datetime.now()
        tz = pytz.timezone('Asia/Kolkata')
        now = now.astimezone(tz)
        end_time = now.strftime("%d/%m/%Y %H:%M:%S")

        with open('session_start.txt', 'r') as f:
            start_time = f.readline()
        f.close()

        with open('drowsiness_count.txt', 'r') as f:
            drowsiness_count = int(f.readline())
        f.close()

        analytics = UserAnalytics(user=request.user, start_time = start_time, end_time=end_time, drowsiness_count=drowsiness_count)
        analytics.save()

    except Exception as e:
        print(e)

    return render(request,'app/service_ended.html',{})

@login_required
def home(request):
    return render(request,'app/home.html',{'user':request.user.username})

@login_required
def analytics(request):
    data = UserAnalytics.objects.order_by('id')
    data = data.filter(user= request.user)
    lables = []
    counts = []
    start_time = []
    end_time = []
    for i in data:
        lables.append(i.start_time)
        counts.append(i.drowsiness_count)
        start_time.append(i.start_time)
        end_time.append(i.end_time)
    return render(request,'app/analytics.html',{'user':request.user.username,'labels':lables,'counts':counts,'start_time':start_time,'end_time':end_time})

def landing(request):
    return render(request,'app/landing.html',{})