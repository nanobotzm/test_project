from django.shortcuts import render
import datetime

def home(request):
    date = datetime.datetime.now().date()
    name = 'Misha'
    received_info = {'date': date, 'name': name}
    return render(request, 'base.html', received_info)
