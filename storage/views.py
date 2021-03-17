from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from employee.models import User
from storage.models import  Thing, UseThing, Composition, Cabinet, Location, StatusThing, Status
from django.db.models import F,  Sum, Q
from employee.views import authView
from storage.forms import ThingForm, UseThingForm, CompositionForm, StatusThingForm
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce

# Главная таблица всего материально-технического обеспечения  
class ThingList(authView, ListView):
    model = Thing
    template_name = "things_list.html"
    context_object_name = 'things'
    paginate_by = 10
    def get_queryset(self):
        # Реализация фильтров по бухгалтерскому учёту, по наименованию, кабинету хранения и ответственным
        query = Q()
        if 'is_accounting' in self.request.GET and self.request.GET['is_accounting']:
            query.add(Q(is_accounting=self.request.GET['is_accounting']), Q.AND)
        if 'is_material' in self.request.GET and self.request.GET['is_material']:
            query.add(Q(is_material=self.request.GET['is_material']), Q.AND)
        if 'name' in self.request.GET:
            query.add(Q(name__icontains=self.request.GET['name']), Q.AND)
        if 'cabinet' in self.request.GET and self.request.GET['cabinet']:
            query.add(Q(location__cabinet__id=self.request.GET['cabinet']), Q.AND)
        if 'status' in self.request.GET and self.request.GET['status']:
            query.add(Q(status_thing__status__id=self.request.GET['status']), Q.AND)
        if 'employee' in self.request.GET and self.request.GET['employee']:
            query.add(Q(use__employee__id=self.request.GET['employee']), Q.AND)
        queryset = Thing.objects.filter(query).annotate(
            count_storage=Coalesce(F("count") - Sum("use__count"),F("count"))).order_by('name')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передача данных, по которым идёт фильтрация таблицы
        params = self.request.GET
        for key, value in params.items():
            if value.isdigit():
                context[key] = int(value)
            else:
                context[key] = value
        # Передача списка кабинетов и сотрудников
        context["cabinets"] = Cabinet.objects.all()
        context["statuses"] = Status.objects.all()
        context["employees"] = User.objects.filter(groups__name='teacher').all()
        return context 

# Детальный просмотр выбранного предмета из таблицы  
class ThingDetail(authView, DetailView):
    model = Thing
    template_name = 'thing_detail.html'
    def get_queryset(self):
        # включение в выборку из базы данных дополнительного поля, 
        # которое считает оставшееся количество предметов на складе
        queryset = Thing.objects.all().annotate(count_storage=Coalesce(F("count") - Sum("use__count"),F("count"))).order_by('name')
        return queryset

# Редактирование выбранного предмета из таблицы
class ThingEdit(authView, UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'thing_edit.html'
    slug_field = 'id'
    default_redirect = '/'
    def get_initial(self):
        # Если местоположение введено в базе данных, 
        # то соответствующие данные отображаются в полях формы
        if self.object.location:
            self.initial.update({ 'location_name': self.object.location.name })
            self.initial.update({ 'location_cabinet': self.object.location.cabinet })
            self.initial.update({ 'location_photo': self.object.location.photo })
        return self.initial
    def form_valid(self, form):
        # Если местоположение введено в базе данных, 
        # то по id находится соответствующая запись в связанной таблице местоположений 
        # и обновляются поля name, cabinet и photo данными с текущей формы
        if self.object.location:
            Location.objects.filter(id=self.object.location.id).update(
                name=form.cleaned_data['location_name'],
                cabinet = form.cleaned_data['location_cabinet'],
                photo = form.cleaned_data['location_photo'])
        # если местоположения не было в базе данных, а пользователь ввёл местоположение, 
        # то создаётся новая запись в базе Location и связь OneToOne с полем location
        elif form.cleaned_data['location_name']:
            location = Location.objects.create(
                name = form.cleaned_data['location_name'],
                cabinet = form.cleaned_data['location_cabinet'],
                photo = form.cleaned_data['location_photo'],)
            form.instance.location = location
        form.save()
        return super(ThingEdit, self).form_valid(form)
    # Реализация перехода на предыдущую страницу после успешного сохранения изменений
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class ThingDelete(authView, DeleteView):
    model = Thing
    template_name = 'thing_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        if self.object.location:
            Location.objects.filter(id=self.object.location.id).delete()
        return self.request.session['previous_page']

class ThingCreate(authView, CreateView):
    model = Thing
    form_class = ThingForm
    template_name = 'thing_edit.html'
    default_redirect = '/'
    def get_initial(self):
        self.initial.update({ 'location_name': ''})
        self.initial.update({ 'location_cabinet': '' })
        self.initial.update({ 'location_photo': '' })
        return self.initial
    def form_valid(self, form):
        location = Location.objects.create(
            name = form.cleaned_data['location_name'],
            cabinet = form.cleaned_data['location_cabinet'],
            photo = form.cleaned_data['location_photo'],)
        form.instance.location = location
        return super(ThingCreate, self).form_valid(form)
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self):
        return self.request.session['previous_page']

class UseThingEdit(authView, UpdateView):
    model = UseThing
    form_class = UseThingForm
    template_name = 'usething_edit.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_initial(self):
        if self.object.location:
            self.initial.update({ 'location_name': self.object.location.name })
            self.initial.update({ 'location_cabinet': self.object.location.cabinet })
            self.initial.update({ 'location_photo': self.object.location.photo })
        return self.initial
    def form_valid(self, form):
        if self.object.location:
            Location.objects.filter(id=self.object.location.id).update(
                name=form.cleaned_data['location_name'],
                cabinet = form.cleaned_data['location_cabinet'],
                photo = form.cleaned_data['location_photo'])
        else:
            location = Location.objects.create(
                name = form.cleaned_data['location_name'],
                cabinet = form.cleaned_data['location_cabinet'],
                photo = form.cleaned_data['location_photo'],)
            form.instance.location = location
        return super(UseThingEdit, self).form_valid(form)
    def get_success_url(self): 
        return self.request.session['previous_page']

class UseThingDelete(authView, DeleteView):
    model = UseThing
    template_name = 'usething_delete.html'
    def get_success_url(self): 
        if self.object.location:
            Location.objects.filter(id=self.object.location.id).delete()
        return reverse_lazy('storage:index')

class UseThingCreate(authView, CreateView):
    model = UseThing
    form_class = UseThingForm
    template_name = 'usething_edit.html'
    default_redirect = '/'
    def get_initial(self):
        self.initial.update({'thing': self.kwargs['thing_pk']})
        return self.initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentthing'] = Thing.objects.filter(pk=self.kwargs['thing_pk']).first()
        return context
    def form_valid(self, form):
        location = Location.objects.create(
            name = form.cleaned_data['location_name'],
            cabinet = form.cleaned_data['location_cabinet'],
            photo = form.cleaned_data['location_photo'],)
        form.instance.location = location
        return super(UseThingCreate, self).form_valid(form)
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class CompositionCreate(authView, CreateView):
    model = Composition
    form_class = CompositionForm
    template_name = 'composition_edit.html'
    default_redirect = '/'
    def get_initial(self):
        initial = super(CompositionCreate, self).get_initial()
        initial.update({'thing': self.kwargs['thing_pk']})
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thing'] = Thing.objects.filter(pk=self.kwargs['thing_pk']).first()
        return context 
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class CompositionEdit(authView, UpdateView):
    model = Composition
    form_class = CompositionForm
    template_name = 'composition_edit.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class CompositionDelete(authView, DeleteView):
    model = Composition
    template_name = 'composition_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class StatusThingCreate(authView, CreateView):
    model = StatusThing
    form_class = StatusThingForm
    template_name = 'statusthing_edit.html'
    default_redirect = '/'
    def get_initial(self):
        initial = super(StatusThingCreate, self).get_initial()
        initial.update({'thing': self.kwargs['thing_pk']})
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thing'] = Thing.objects.filter(pk=self.kwargs['thing_pk']).first()
        return context 
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class StatusThingEdit(authView, UpdateView):
    model = StatusThing
    form_class = StatusThingForm
    template_name = 'statusthing_edit.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class StatusThingDelete(authView, DeleteView):
    model = StatusThing
    template_name = 'statusthing_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']
    def get_success_url(self): 
        return reverse_lazy('storage:thing_detail', kwargs={'pk': self.kwargs['thing_pk']})