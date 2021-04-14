from rest_framework import serializers
from sumassess.models import Programm, SubjectGroup, Subject, Criteria, \
    Strand, ClassYear, Objective, Level

class ProgrammSerializer(serializers.ModelSerializer): 
    class Meta:  
        model = Programm  
        fields = ['name_eng', 'name_rus', 'label']

class SubjectGroupSerializer(serializers.ModelSerializer): 
    programm = ProgrammSerializer(required=False)
    class Meta:  
        model = SubjectGroup  
        fields = ['id', 'name_eng', 'name_rus', 'programm', 'picture', 'schema']

class CriteriaSerializer(serializers.ModelSerializer): 
    ibgroup = SubjectGroupSerializer(required=False)
    class Meta:  
        model = Criteria  
        fields = ['id', 'name_eng', 'name_rus', 'letter', 'ibgroup', 'picture']

class StrandSerializer(serializers.ModelSerializer):
    letter = serializers.CharField(source='get_letter_display')
    criteria = CriteriaSerializer(required=False)
    class Meta:  
        model = Strand  
        fields = ['id', 'name_eng', 'name_rus', 'letter', 'number', 'shortname_eng', 'shortname_rus', 'criteria']

class ClassYearSerializer(serializers.ModelSerializer): 
    programm = ProgrammSerializer(required=False)
    class Meta:  
        model = ClassYear  
        fields = ['id', 'year_ib', 'year_rus', 'programm']

class ObjectiveSerializer(serializers.ModelSerializer): 
    year = ClassYearSerializer(required=False)
    strand = StrandSerializer(required=False)
    class Meta:  
        model = Objective  
        fields = ['id', 'year', 'strand', 'name_eng', 'name_rus']

class LevelSerializer(serializers.ModelSerializer): 
    objective = ObjectiveSerializer(required=False)
    class Meta:  
        model = Level  
        fields = ['id', 'name_eng', 'name_rus', 'point', 'objective']