import django_filters
from django import forms
from employee.models import User
from storage.models import Thing, Location
from django.db import models


class ThingFilter(django_filters.FilterSet):
    name_manufacturer = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30, 'placeholder':'Введите название'}), lookup_expr='icontains')
    base_location = django_filters.ModelChoiceFilter(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Кабинет")
    finresp = django_filters.ModelChoiceFilter(queryset=User.objects.filter(groups__name='teacher').all(), widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Ответственный")

    class Meta:
        model = Thing
        exclude = ['photo', 'photo_base_location']
        fields = ['name_manufacturer', 'base_location', 'finresp']