from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from sumassess.models import Subject, YearIB, Criteria, Objective, Level, Unit, Strand, Student, Group, SubGroup, AssessmentUnit, StudyYear, SubjectGroup, Period, AssessmentUnitLevel

# класс для импорта Objective
class ObjectiveResource(resources.ModelResource):
    class Meta:
        model = Objective

# класс для импорта LEVEL
class LevelResource(resources.ModelResource):
    class Meta:
        model = Level

# класс для импорта Strand
class StrandResource(resources.ModelResource):
    class Meta:
        model = Strand

# класс для импорта Group
class GroupResource(resources.ModelResource):
    class Meta:
        model = Group

# класс для импорта SubGroup
class SubGroupResource(resources.ModelResource):
    class Meta:
        model = SubGroup

# класс для импорта Student
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

# класс для импорта YearIB
class YearIBResource(resources.ModelResource):
    class Meta:
        model = YearIB

# класс для импорта Criteria
class CriteriaResource(resources.ModelResource):
    class Meta:
        model = Criteria

# класс для импорта Period
class PeriodResource(resources.ModelResource):
    class Meta:
        model = Period

@admin.register(Objective)
class ObjectiveAdmin(ImportExportActionModelAdmin):
    resource_class = ObjectiveResource
    list_display = ('year_ib', 'criteria', 'strand', 'name', 'name_rus')

@admin.register(Level)
class LevelAdmin(ImportExportActionModelAdmin):
    resource_class = LevelResource
    list_display = ('objective', 'name', 'name_rus', 'id','point')

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('programm', 'name', 'name_rus')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subjgroup', 'id_dnevnik')

# @admin.register(YearIB)
# class YearIBAdmin(admin.ModelAdmin):
#     list_display = ('programm', 'year_ib', 'grade_rus')
@admin.register(YearIB)
class YearIBAdmin(ImportExportActionModelAdmin):
    resource_class = YearIBResource
    list_display = ('programm', 'year_ib', 'grade_rus')

# @admin.register(Criteria)
# class CriteriaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'name_rus', 'letter', 'subject')
@admin.register(Criteria)
class CriteriaAdmin(ImportExportActionModelAdmin):
    resource_class = CriteriaResource
    list_display = ('name', 'name_rus', 'letter', 'subject')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_ib', 'teacher', 'subject')
    filter_horizontal = ('objective',) 

# @admin.register(Strand)
# class StrandAdmin(admin.ModelAdmin):
#     list_display = ('name', 'name_rus', 'num', 'letter')
@admin.register(Strand)
class StrandAdmin(ImportExportActionModelAdmin):
    resource_class = StrandResource
    list_display = ('shortname', 'shortname_rus', 'num', 'letter', 'criteria')

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('surname', 'name', 'group')
@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin):
    resource_class = StudentResource
    list_display = ('shortname', 'id', 'group')
    
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('year', 'letter', 'styear')
@admin.register(Group)
class GroupAdmin(ImportExportActionModelAdmin):
    resource_class = GroupResource
    list_display = ('id', 'year', 'letter', 'styear')

# @admin.register(SubGroup)
# class SubGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'group', 'teacher')
@admin.register(SubGroup)
class SubGroupAdmin(ImportExportActionModelAdmin):
    resource_class = SubGroupResource
    list_display = ('id', 'name', 'group', 'subject','teacher')

@admin.register(Period)
class PeriodAdmin(ImportExportActionModelAdmin):
    resource_class = PeriodResource
    list_display = ('name', 'data_start', 'data_end','id_dnevnik', 'styear')

@admin.register(StudyYear)
class StudyYearAdmin(admin.ModelAdmin):
    list_display = ('year',)


@admin.register(AssessmentUnit)
class AssessmentUnitAdmin(admin.ModelAdmin):
    list_display = ('student', 'unit', 'mark_a', 'mark_b', 'mark_c', 'mark_d')
    filter_horizontal = ('level',) 

@admin.register(AssessmentUnitLevel)
class AssessmentUnitLevelAdmin(admin.ModelAdmin):
    list_display = ('assessmentunit', 'level', 'comment')