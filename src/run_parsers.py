import asyncio
import codecs

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from myapp.parsers import *
import os, sys


path_proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(path_proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django
django.setup()

from myapp.models import Vacancy, City, Language, Error, URL

User = get_user_model()

parsers = ((work, 'work'),
           (rabota, 'rabota'),
           (dou, 'dou'),
           (djinni, 'djinni'))

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

vacancies, errors = [], []


def get_settings():
    qs = User.objects.filter(mailing=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_url(_settings):
    qs = URL.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    vac, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    vacancies.extend(vac)


settings = get_settings()
url_list = get_url(settings)
# import time
#
# start = time.time()
loop = asyncio.get_event_loop()
tmp_task = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         v, e = func(url, city=data['city'], language=data['language'])
#         vacancies += v
#         errors += e

loop.run_until_complete(tasks)
loop.close()
# print(time.time()-start)
for vac in vacancies:
    v = Vacancy(**vac)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    e = Error(data=errors).save()
# with codecs.open('work.txt', 'w', 'utf-8') as file:
#     file.write(str(vacancies))

