from django.db.models.expressions import OrderBy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from employee.models import User
from storage.models import  Thing, UseThings, Equipment, CompositionEquipment
from django.db.models import F,  Sum
from employee.views import authView
from storage.forms import ThingForm, UseThingsForm, EquipmentForm, ComposEquipmentForm
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from django_filters.views import FilterView
from storage.filters import ThingFilter

class CountThing():
    def get_queryset(self):
        queryset = Thing.objects.all().annotate(count_storage=Coalesce(F("count") - Sum("use_thing__count"),F("count"))).order_by('name_manufacturer')
        return queryset

class ThingList(authView, CountThing, FilterView):
    model = Thing
    template_name = "things_list.html"
    filterset_class = ThingFilter
    context_object_name = 'things'
    paginate_by = 30
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['things'] = ThingFilter(self.request.GET, queryset=Thing.objects.order_by('name_manufacturer')).qs
    #     return context

class ThingDetail(authView, CountThing, DetailView):
    model = Thing
    template_name = 'things_detail.html'

class ThingEdit(authView, UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things_edit.html'
    slug_field = 'id'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class ThingDelete(authView, DeleteView):
    model = Thing
    template_name = 'things_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class ThingCreate(authView, CreateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things_edit.html'
    success_url = reverse_lazy('storage:things')

class EquipmentCreate(authView, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment_edit.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class EquipmentEdit(authView, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment_edit.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class EquipmentDelete(authView, DeleteView):
    model = Equipment
    template_name = 'equipment_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

# Добавление элемента в состав позиции
class CompositionEquipmentCreate(authView, CreateView):
    model = CompositionEquipment
    form_class = ComposEquipmentForm
    template_name = 'compos_equipment_edit.html'
    def get_initial(self):
        initial = super(CompositionEquipmentCreate, self).get_initial()
        if self.request.GET['thing']:
            initial.update({'thing': self.request.GET['thing']})
        return initial
    def get_success_url(self): 
        return reverse_lazy('storage:things_detail', args = (self.request.GET['thing'],))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET['thing']:
            context['thing'] = Thing.objects.filter(pk=self.request.GET['thing']).first()
        return context 

# Редактирование элемента в составе позиции
class CompositionEquipmentEdit(authView, UpdateView):
    model = CompositionEquipment
    form_class = ComposEquipmentForm
    template_name = 'compos_equipment_edit.html'
    def get_success_url(self): 
        return reverse_lazy('storage:things_detail', args = (self.get_object().thing.id,))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thing'] = Thing.objects.filter(pk=self.get_object().thing.id).first()
        return context 

# Удаление элемента из состава позиции
class CompositionEquipmentDelete(authView, DeleteView):
    model = CompositionEquipment
    template_name = 'compos_equipment_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

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
