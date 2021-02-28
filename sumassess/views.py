from django.shortcuts import render
from rest_framework import generics
from sumassess.models import Objective, Criteria, YearIB, Unit, AssessmentUnit, Student, Group, StudyYear, Level, Period
from sumassess.serializers import ObjectiveSerializer, CriteriaSerializer, YearIBSerializer, UnitSerializer, StudentSerializer, \
    GroupSerializer, LevelSerializer, AssessmentUnitSerializer
from employee.views import authView
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView  
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from datetime import date
from django.db.models import Q
from rest_framework.response import Response
from sumassess.forms import UnitForm
import json
from django.core import serializers
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Case, SmallIntegerField, Value, When
from django import template
import requests
import collections
from django.template.defaulttags import register

@register.filter
def get_id_dnevnik(dictionary, st):
    if isinstance(dictionary,dict):
        return dictionary.get(st.student.id_dnevnik) or 0
    else: 
        return '-'

@register.simple_tag
def final_mark(sum_assessment, marks, student):
    if isinstance(sum_assessment,dict):
        average_mark = marks.get(student.id_dnevnik)
        mark = round((sum_assessment or 0)* 0.6 + (average_mark or 0) * 0.4, 2)
        return mark
    else: 
        return 0

# @register.filter
# def final_mark(sum_assessment, marks, student):
#     average_mark = marks.get(student.student.id_dnevnik)
#     mark = sum_assessment * 0.6 + average_mark * 0.4
#     return mark or 2

def criteria_page(request):
    return render(request, 'view_criteria.html')

class YearIBView(generics.ListCreateAPIView):
    queryset = YearIB.objects.all()
    serializer_class = YearIBSerializer

class CriteriaView(generics.ListCreateAPIView):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer

class ObjectiveView(generics.ListAPIView):
    serializer_class = ObjectiveSerializer
    def get_queryset(self):
        year = self.request.GET['year']
        if self.request.GET.get('unit'):
            unit = self.request.GET['unit']
            queryset = Objective.objects.filter(year_ib__year_ib=year, unit_objective__id=unit)
        else:
            queryset = Objective.objects.filter(year_ib__year_ib=year)
        return queryset.order_by('strand')

class StudentView(generics.ListAPIView):
    serializer_class = StudentSerializer
    def get_queryset(self):
        group = self.request.GET['group']
        queryset = Student.objects.filter(group__id=group)
        return queryset.order_by('shortname')

class GroupView(generics.ListAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self):
        group = self.request.GET['group']
        queryset = Group.objects.filter(id=group)
        return queryset

class LevelView(generics.ListAPIView):
    serializer_class = LevelSerializer
    def get_queryset(self):
        id_year = self.request.GET['year']
        id_unit = self.request.GET['unit']
        queryset = Level.objects.filter(objective__year_ib__id=id_year, objective__unit_objective__id=id_unit)
        return queryset

def student_page(request):
    return render(request, 'view_students.html')

class UnitList(authView, ListView):
    model = Unit
    context_object_name = "units"
    template_name = "unit_list.html"
    def get_queryset(self):
        user = self.request.user.id
        if 'period' in self.request.GET:
            current_period = self.request.GET['period']
            print(current_period)
            queryset = Unit.objects.filter(teacher__id=user, period=current_period)
        else:
            queryset = Unit.objects.filter(teacher__id=user)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = StudyYear.objects.filter(Q(data_start__lte=date.today()) & Q(data_end__gte=date.today())).first()
        periods = Period.objects.filter(styear=year.id)
        if 'period' in self.request.GET:
            context['current_period'] = int(self.request.GET['period'])
        context['current_year'] = year
        context['periods'] = periods
        return context 

class UnitCreate(authView, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'unit_edit.html'
    default_redirect = '/'
    def get_initial(self):
        self.initial.update({ 'user': self.request.user })
        year = StudyYear.objects.filter(Q(data_start__lte=date.today()) & Q(data_end__gte=date.today())).first()
        self.initial.update({ 'year': year })
        return self.initial
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class UnitEdit(authView, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'unit_edit.html'
    slug_field = 'id'
    default_redirect = '/'
    register = template.Library()
    def get_initial(self):
        print(self.object.name)
        self.initial.update({ 'year_ib': self.object.year_ib })
        return self.initial
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # obj_data = [x.id for x in self.object.objective.all()]
        # context['obj_data'] = obj_data
        return context 

class UnitDetail(authView, DetailView):
    model = Unit
    template_name = 'unit_detail.html'

class UnitDelete(authView, DeleteView):
    model = Unit
    template_name = 'unit_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']

class AssessmentUnitList(authView, ListView):
    model = AssessmentUnit
    context_object_name = "students"
    template_name = "unit_students.html"
    # при POST-запросе добавление выбранных студентов в базу оценок текущего юнита
    def post(self, request, *args, **kwargs):
        data = request.POST
        unit = request.POST.get('unit', False);
        if unit and data:
            for key, value in data.items():
                if 'student' in key:
                    query = AssessmentUnit.objects.create(student=Student.objects.get(id=int(value)),
                                                        unit=Unit.objects.get(id=unit))
                    query.save()
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)
    def get_queryset(self):
        range_criterion = {
            1: { 2: 0, 3: 3, 4: 5, 5: 7 },
            2: { 2: 0, 3: 6, 4: 10, 5: 14 },
            3: { 2: 0, 3: 8, 4: 14, 5: 20 },
            4: { 2: 0, 3: 11, 4: 19, 5: 28 },
        }

        unit = self.request.GET['unit']
        group = self.request.GET['class']
        teacher = self.request.user.id
        # получение количества критериев в текущем юните
        current_unit = Unit.objects.filter(id=unit).first()
        criteria = set()
        for data in current_unit.objective.all():
            criteria.add(data.criteria.letter)
        
        # выборка журнала по текущему юниту, группе студентов и учителю
        queryset = AssessmentUnit.objects.filter(unit=unit, student__group=group, unit__teacher=teacher)
        # добавление поля суммы баллов по всем критериям
        queryset = queryset.annotate(sum_mark=F('mark_a') + F('mark_b') + F('mark_c') + F('mark_d'))
        # добавление поля российской оценки по сумме критериев
        if len(criteria):
            range_rus_mark = range_criterion[len(criteria)]
            queryset = queryset.annotate(rus_mark=Case(
                When(sum_mark__gte=range_rus_mark[5], then=Value(5)),
                When(sum_mark__gte=range_rus_mark[4], then=Value(4)),
                When(sum_mark__gte=range_rus_mark[3], then=Value(3)),
                When(sum_mark__gte=range_rus_mark[2], then=Value(2)),
                default=Value(0),
                output_field=SmallIntegerField()))
        
        self.myqueryset = queryset
        return queryset.order_by('student')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.request.GET['class']
        unit_id = self.request.GET['unit']
        if unit_id and group_id:
            unit_data = Unit.objects.filter(pk=unit_id).first()
            objectives = set ()
            for data in unit_data.objective.all():
                objectives.add(data.criteria.letter)
            context['unit_data'] = unit_data
            context['objectives'] = sorted(list(objectives))
            group_data = Group.objects.filter(pk=group_id).first()
            context['group_data'] = group_data
        
            # Запрос к Dnevnik.ru
            url_dnevnik_api ='https://api.dnevnik.ru/v2.0/'
            group = group_data.group_dnevnik
            subject = unit_data.subject.id_dnevnik
            from_data = unit_data.period.data_start
            to_data = unit_data.period.data_end
            headers = {'Access-Token': 'QT1UAaAANqjnFtQGuWgzFzc1fo5BqOyt',
                        'Content-Type': 'application/json'}
            url = "{}edu-groups/{}/subjects/{}/marks/{}/{}".format(url_dnevnik_api, group, subject, from_data, to_data)
            data = requests.get(url, headers=headers)
            student_marks = {}
            count_marks = collections.Counter()

            if data.status_code == 200:
                for student in data.json():
                    print(student['person_str'])
                    count_marks[student['person_str']] += 1
                    if student['value'] != 'NA':
                        if student['value'][-1].isdigit():
                            student_marks[student['person_str']] = student_marks.get(student['person_str'], 0) + int(student['value'])
                        else:
                            student_marks[student['person_str']] = student_marks.get(student['person_str'], 0) + int(student['value'][0])
                for student, mark in student_marks.items():
                    student_marks[student] = round(mark / count_marks[student],2)
                context['student_marks'] = student_marks
            else:
                print('Дневник.РУ не отвечает!')
        return context 

# API для получения сведений о юните и обновлении Objective
class UnitView(APIView):
    # Просмотр сведений о выбранном юните
    def get(self, request, pk=None):
        posts = get_object_or_404(Unit.objects.all(), pk=pk)
        serializer = UnitSerializer(posts)
        return Response(serializer.data)
    # Обновление данных об Objective в выбранном юните
    def put(self, request, pk):
        saved_unit = get_object_or_404(Unit.objects.all(), pk=pk)
        data = request.data
        saved_unit.objective.clear()
        for obj in data['obj']:
            objective = Objective.objects.get(id=obj)
            saved_unit.objective.add(objective)
        serializer = UnitSerializer(instance=saved_unit, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            unit_saved = serializer.save()
        
        # Получение всех записей журнала текущего юнита
        assess_units = AssessmentUnit.objects.filter(unit__id=pk).all()
        # Перебор записей журнала, фильтрация добавленных в них уровней достижений по тем, 
        # которые не входят в актуальные objectives и их удаление

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Удаляться должны не из самой таблицы level, а из ManyToMany (может, заменить на remove)
        for assess_unit in assess_units:
            pass
            # assess_unit.level.filter(~Q(objective__id__in=data['obj'])).clear()
        return Response({'Success': "Unit {} updated successfully".format(unit_saved.name)})



class AssessmentUnitDelete(authView, DeleteView):
    model = AssessmentUnit
    template_name = 'unit_student_delete.html'
    default_redirect = '/'
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)
    def get_success_url(self): 
        return self.request.session['previous_page']


# class AssessmentUnitEdit(authView, UpdateView):
#     model = AssessmentUnit
#     template_name = 'unit_student_edit.html'
#     form_class = AssessmentUnitForm
#     slug_field = 'id'
#     default_redirect = '/'
#     def get(self, request, *args, **kwargs):
#         request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
#         return super().get(request, *args, **kwargs)
#     def get_success_url(self): 
#         return self.request.session['previous_page']

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

def unit_assessment_page(request, id_assessstudent, id_year, id_unit):
    selected_student = AssessmentUnit.objects.get(id=id_assessstudent)
    current_year = YearIB.objects.get(id=id_year)
    current_unit = Unit.objects.get(id=id_unit)
    correct_level = Level.objects.filter(objective__year_ib__id=id_year).values()
    context = {
        'selected_student': selected_student,
        'current_year': current_year,
        'current_unit': current_unit,
        'correct_level': json.dumps(list(correct_level)),
        }
    context['show_login'] = True
    if request.user.is_authenticated:  
        context['username'] = request.user.username
    return render(request, 'unit_assessment_page.html', context)


# API для добавления level в AssessmentUnit
class AssessmentUnitView(APIView):
    # Просмотр сведений о выбранной записи
    def get(self, request, pk=None):
        posts = get_object_or_404(AssessmentUnit.objects.all(), pk=pk)
        serializer = AssessmentUnitSerializer(posts)
        return Response(serializer.data)

    def put(self, request, pk):
        saved_assess_unit = get_object_or_404(AssessmentUnit.objects.all(), pk=pk)
        data = request.data
        saved_assess_unit.level.clear()
        for le in data['level']:
            if 'id' in le:
                level = Level.objects.get(id=le['id'])
                saved_assess_unit.level.add(level)
        serializer = AssessmentUnitSerializer(instance=saved_assess_unit, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            assess_unit_saved = serializer.save()
        return Response({'Success': "Updated successfully"})
