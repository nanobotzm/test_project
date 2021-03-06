from django.shortcuts import render
from .models import Vacancy

def home_view(request):
    querySet = Vacancy.objects.all()
    return render(request, 'myapp/home.html', {'object_list': querySet})
