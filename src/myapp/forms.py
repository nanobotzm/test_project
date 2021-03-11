from django import forms

from myapp.models import City, Language


class FindForm(forms.Form):
    # city = forms.CharField(initial='class')
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Вакансия')
