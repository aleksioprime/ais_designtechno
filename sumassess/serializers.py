from rest_framework import serializers
from sumassess.models import Objective, Criteria, YearIB, Unit, Strand, Student, Group, AssessmentUnit, Level

class YearIBSerializer(serializers.ModelSerializer): 
    class Meta:  
        model = YearIB  
        fields = ['id', 'year_ib', 'programm', 'grade_rus']

class StrandSerializer(serializers.ModelSerializer): 
    criteria = serializers.StringRelatedField(read_only=True)
    class Meta:  
        model = Strand  
        fields = ['num', 'letter', 'name', 'name_rus', 'shortname', 'shortname_rus', 'criteria']

class CriteriaSerializer(serializers.ModelSerializer):  
    subject = serializers.StringRelatedField(read_only=True)
    letter = serializers.StringRelatedField(read_only=True)   
    name = serializers.StringRelatedField(read_only=True) 
    name_rus = serializers.StringRelatedField(read_only=True) 
    class Meta:  
        model = Criteria  
        fields = ['subject', 'letter', 'name', 'name_rus']

class ObjectiveSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer(required=False)
    year_ib = YearIBSerializer(required=False)
    strand = StrandSerializer(required=False)
    class Meta:
        model = Objective
        fields = ['id', 'year_ib', 'criteria', 'criteria', 'strand', 'name', 'name_rus']

class UnitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    teacher = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    objective = ObjectiveSerializer(required=False, many=True)
    year_ib = YearIBSerializer(required=False)

    def create(self, validated_data):
        return Unit.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.save()
        return instance

class GroupSerializer(serializers.ModelSerializer):
    year = YearIBSerializer(required=False)
    class Meta:
        model = Group
        fields = ['year','styear', 'group_dnevnik', 'letter', 'info']

class LevelSerializer(serializers.ModelSerializer):  
    objective = ObjectiveSerializer()
    class Meta:  
        model = Level  
        fields = ['id', 'objective', 'name', 'name_rus', 'point']

# class AssessmentUnitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AssessmentUnit
#         fields = ['id','student','unit','level']

class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(required=False)
    class Meta:
        model = Student
        fields = ['id', 'shortname','name', 'surname', 'gender', 'group', 'assessment_student']

class AssessmentUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    unit = UnitSerializer(required=False)
    student = StudentSerializer(required=False)
    level = LevelSerializer(required=False, many=True)
    mark_a = serializers.IntegerField()
    mark_b= serializers.IntegerField()
    mark_c = serializers.IntegerField()
    mark_d = serializers.IntegerField()

    def create(self, validated_data):
        return AssessmentUnit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mark_a = validated_data.get('mark_a', instance.mark_a)
        instance.mark_b = validated_data.get('mark_b', instance.mark_b)
        instance.mark_c = validated_data.get('mark_c', instance.mark_c)
        instance.mark_d = validated_data.get('mark_d', instance.mark_d)
        instance.save()
        return instance
