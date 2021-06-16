from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from sumassess.models import Programm, SubjectGroup, Subject, Criteria, Strand, ClassYear, Objective, Level, Student

# ресурс для экспорта-импорта Programm
class ProgrammResource(resources.ModelResource):
    class Meta:
        model = Programm

# ресурс для экспорта-импорта SubjectGroup
class SubjectGroupResource(resources.ModelResource):
    class Meta:
        model = SubjectGroup

# ресурс для экспорта-импорта Subject
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject

# ресурс для экспорта-импорта Criteria
class CriteriaResource(resources.ModelResource):
    class Meta:
        model = Criteria

# ресурс для экспорта-импорта Strand
class StrandResource(resources.ModelResource):
    class Meta:
        model = Strand

# ресурс для экспорта-импорта ClassYear
class ClassYearResource(resources.ModelResource):
    class Meta:
        model = ClassYear

# ресурс для экспорта-импорта Objective
class ObjectiveResource(resources.ModelResource):
    class Meta:
        model = Objective

# ресурс для экспорта-импорта Level
class LevelResource(resources.ModelResource):
    class Meta:
        model = Level

# ресурс для экспорта-импорта Student
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

@admin.register(Programm)
class ProgrammAdmin(ImportExportActionModelAdmin):
    resource_class = ProgrammResource
    list_display = ('label', 'name_eng', 'name_rus')

@admin.register(SubjectGroup)
class SubjectGroupAdmin(ImportExportActionModelAdmin):
    resource_class = SubjectGroupResource
    list_display = ('name_eng', 'name_rus', 'programm')

@admin.register(Subject)
class SubjectAdmin(ImportExportActionModelAdmin):
    resource_class = SubjectResource
    list_display = ('name_eng', 'name_rus', 'ibgroup')

@admin.register(Criteria)
class CriteriaAdmin(ImportExportActionModelAdmin):
    resource_class = CriteriaResource
    list_display = ('name_eng', 'name_rus', 'letter', 'ibgroup')

@admin.register(Strand)
class StrandAdmin(ImportExportActionModelAdmin):
    resource_class = StrandResource
    list_display = ('shortname_eng', 'shortname_rus', 'letter', 'criteria')

@admin.register(ClassYear)
class ClassYearAdmin(ImportExportActionModelAdmin):
    resource_class = ClassYearResource
    list_display = ('year_ib', 'year_rus', 'programm')

@admin.register(Objective)
class ObjectiveAdmin(ImportExportActionModelAdmin):
    resource_class = ObjectiveResource
    list_display = ('strand', 'year', 'name_eng', 'name_rus')

@admin.register(Level)
class LevelAdmin(ImportExportActionModelAdmin):
    resource_class = LevelResource
    list_display = ('name_eng', 'objective')

@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin):
    resource_class = StudentResource
    list_display = ('user', 'gender')