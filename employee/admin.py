from django.contrib import admin
from employee.models import User, LogNoteBook
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

# класс ресурса для создания импорта-экспорта
class UserResource(resources.ModelResource):
    class Meta:
        model = User

# класс ресурса для создания импорта-экспорта
class LogNoteBookResource(resources.ModelResource):
    class Meta:
        model = LogNoteBook

@admin.register(User)
class EmployeeAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'surname', 'name', 'patronymic', 'position', 'id_card')

# @admin.register(User)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('username', 'surname', 'name', 'patronymic', 'position')

@admin.register(LogNoteBook)
class LogNoteBookAdmin(ImportExportActionModelAdmin):
    resource_class = LogNoteBookResource
    list_display = ('date', 'location', 'employee')
