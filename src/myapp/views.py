from django.shortcuts import render

from .models import Vacancy
from .forms import FindForm


def home_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')  # Киев
    language = request.GET.get('language')  # Python
    form_request = dict()
    if city or language:
        if city:
            form_request['city__slug'] = city
        if language:
            form_request['language__slug'] = language
    querySet = Vacancy.objects.filter(**form_request)
    return render(request, 'myapp/home.html', {'object_list': querySet,
                                                'form': form})
