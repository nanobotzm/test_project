import codecs
from myapp.parsers import *

parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'),
           (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
           (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'))


vacancies, errors = [], []
for func, url in parsers:
    v, e = func(url)
    vacancies += v
    errors += e

with codecs.open('work.txt', 'w', 'utf-8') as file:
    file.write(str(vacancies))
