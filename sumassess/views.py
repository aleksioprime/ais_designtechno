from django.shortcuts import render
from sumassess.models import Programm, SubjectGroup, Criteria, \
    Strand, ClassYear, Objective, Level
from sumassess.serializers import SubjectGroupSerializer, CriteriaSerializer, \
    StrandSerializer, ClassYearSerializer, ObjectiveSerializer, LevelSerializer
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView 

def myp_subject_criteria(request):
    context = {'subject': SubjectGroup.objects.get(name_eng__icontains='Design')}
    context['show_login'] = True
    if request.user.is_authenticated:  
        context['username'] = request.user.username
    return render(request, 'myp_subject_criteria.html', context)

class SubjectGroupView(APIView):
    def get(self, request):
        if self.request.GET.get('programm'):
            programm = self.request.GET['programm']
            data = SubjectGroup.objects.filter(programm=programm)
            serializer = SubjectGroupSerializer(data, many=True)
        return Response(serializer.data)

class CriteriaView(APIView):
    def get(self, request):
        if self.request.GET.get('sg'):
            sg = self.request.GET['sg']
            data = Criteria.objects.filter(ibgroup=sg)
            serializer = CriteriaSerializer(data, many=True)
        return Response(serializer.data)

class StrandView(APIView):
    def get(self, request):
        if self.request.GET.get('sg'):
            sg = self.request.GET['sg']
            data = Strand.objects.filter(criteria__ibgroup=sg)
            serializer = StrandSerializer(data, many=True)
        return Response(serializer.data)

class ClassYearView(APIView):
    def get(self, request):
        if self.request.GET.get('programm'):
            programm = self.request.GET['programm']
            data = ClassYear.objects.filter(programm=programm)
            serializer = ClassYearSerializer(data, many=True)
        return Response(serializer.data)

class ObjectiveView(APIView):
    def get(self, request):
        if self.request.GET.get('year'):
            year = self.request.GET['year']
            if self.request.GET.get('criterion'):
                criterion = self.request.GET['criterion']
                data = Objective.objects.filter(year=year, strand__criteria=criterion)
            else:
                data = Objective.objects.filter(year=year)
            serializer = ObjectiveSerializer(data, many=True)
        elif self.request.GET.get('strand'):
            strand = self.request.GET['strand']
            data = Objective.objects.filter(strand=strand)
            serializer = ObjectiveSerializer(data, many=True)
        return Response(serializer.data)

class LevelView(APIView):
    def get(self, request):
        if self.request.GET.get('year'):
            year = self.request.GET['year']
            if self.request.GET.get('criterion'):
                criterion = self.request.GET['criterion']
                data = Level.objects.filter(objective__year=year, objective__strand__criteria=criterion).order_by('-point')
            else:
                data = Level.objects.filter(objective__year=year).order_by('-point')
        elif self.request.GET.get('strand'):
            strand = self.request.GET['strand']
            data = Level.objects.filter(objective__strand=strand).order_by('-point')
        else:
            data = Level.objects.all().order_by('-point')
        serializer = LevelSerializer(data, many=True)
        return Response(serializer.data)