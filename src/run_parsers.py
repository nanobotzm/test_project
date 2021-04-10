import codecs

from django.db import DatabaseError

from myapp.parsers import *
import os, sys


path_proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(path_proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django
django.setup()

from myapp.models import Vacancy, City, Language, Error

parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
           (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'))

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

vacancies, errors = [], []
for func, url in parsers:
    v, e = func(url)
    vacancies += v
    errors += e

for vac in vacancies:
    v = Vacancy(**vac, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    e = Error(data=errors).save()
# with codecs.open('work.txt', 'w', 'utf-8') as file:
#     file.write(str(vacancies))
