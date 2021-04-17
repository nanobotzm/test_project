from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    # qs = []
    form_request = dict()
    if city or language:
        if city:
            form_request['city__slug'] = city
        if language:
            form_request['language__slug'] = language

    queryset = Vacancy.objects.filter(**form_request)
    return render(request, 'test_check/home.html', {'object_list': queryset,
                                                    'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    form_request = dict()
    if city or language:
        if city:
            form_request['city__slug'] = city
        if language:
            form_request['language__slug'] = language

    queryset = Vacancy.objects.filter(**form_request)
    paginator = Paginator(queryset, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html', {'object_list': page_obj,
                                                    'form': form})
