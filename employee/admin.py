from django.contrib import admin
from employee.models import User
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

# класс ресурса для создания импорта-экспорта
class UserResource(resources.ModelResource):
    class Meta:
        model = User

@admin.register(User)
class EmployeeAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'surname', 'name', 'patronymic', 'position')

# @admin.register(User)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('username', 'surname', 'name', 'patronymic', 'position')

