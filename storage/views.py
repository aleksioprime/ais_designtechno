from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from employee.models import User
from storage.models import  Thing, UseThings
from django.db.models import F,  Sum
from employee.views import authView
from storage.forms import ThingForm, UseThingsForm
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from django_filters.views import FilterView
from storage.filters import ThingFilter

class CountThing():
    def get_queryset(self):
        queryset = Thing.objects.all().annotate(count_storage=Coalesce(F("count") - Sum("use_thing__count"),F("count")))
        return queryset

class ThingList(authView, CountThing, FilterView):
    model = Thing
    context_object_name = "things"
    template_name = "things_list.html"
    filterset_class = ThingFilter
    paginate_by = 20
    ordering = ['id']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     filter = ThingFilter(self.request.GET, queryset=Thing.objects.all())
    #     context['filter'] = filter
    #     return context 

class ThingDetail(authView, CountThing, DetailView):
    model = Thing
    template_name = 'things_detail.html'

class ThingEdit(authView, UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things_edit.html'
    slug_field = 'id'
    success_url = reverse_lazy('storage:things')

class ThingDelete(authView, DeleteView):
    model = Thing
    template_name = 'things_delete.html'
    success_url = reverse_lazy('storage:things')

class ThingCreate(authView, CreateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things_edit.html'
    success_url = reverse_lazy('storage:things')

class UseThingsEdit(authView, UpdateView):
    model = UseThings
    form_class = UseThingsForm
    template_name = 'usethings_edit.html'
    slug_field = 'id'
    success_url = reverse_lazy('storage:things')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UseThingsDelete(authView, DeleteView):
    model = UseThings
    template_name = 'usethings_delete.html'
    success_url = reverse_lazy('storage:things')

class UseThingsCreate(authView, CreateView):
    model = UseThings
    form_class = UseThingsForm
    template_name = 'usethings_edit.html'
    success_url = reverse_lazy('storage:things')
    def get_initial(self):
        initial = super(UseThingsCreate, self).get_initial()
        if self.request.GET['thing']:
            initial.update({'thing': self.request.GET['thing']})
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET['thing']:
            context['currentthing'] = Thing.objects.filter(pk=self.request.GET['thing']).first()
        return context 
