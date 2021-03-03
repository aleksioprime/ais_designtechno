from django.contrib import admin
from storage.models import Thing, UseThings, Equipment, StatusEquipment, Location, CompositionEquipment, Status
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


# @admin.register(Thing)
# class ThingAdmin(admin.ModelAdmin):
#     list_display = ('name_manufacturer', 'count')

# класс ресурса для создания импорта-экспорта
class ThingResource(resources.ModelResource):
    class Meta:
        model = Thing

# класс ресурса для создания импорта-экспорта
class LocationResource(resources.ModelResource):
    class Meta:
        model = Location

# класс ресурса для создания импорта-экспорта
class EquipmentResource(resources.ModelResource):
    class Meta:
        model = Equipment

# класс ресурса для создания импорта-экспорта
class CompositionEquipmentResource(resources.ModelResource):
    class Meta:
        model = CompositionEquipment

# класс ресурса для создания импорта-экспорта
class StatusResource(resources.ModelResource):
    class Meta:
        model = Status

# класс модели 
@admin.register(Thing)
class ThingAdmin(ImportExportActionModelAdmin):
    resource_class = ThingResource
    list_display = ['name_manufacturer', 'manufacturer', 'inventory_number', 'price', 'count', 'base_location', 'finresp', 'id']

@admin.register(Location)
class LocationAdmin(ImportExportActionModelAdmin):
    resource_class = LocationResource
    list_display = ('label', 'name')

@admin.register(UseThings)
class UseThingsAdmin(admin.ModelAdmin):
    list_display = ('thing', 'employee', 'count')

@admin.register(Equipment)
class EquipmentAdmin(ImportExportActionModelAdmin):
    resource_class = EquipmentResource
    list_display = ('name',)

@admin.register(CompositionEquipment)
class CompositionEquipmentAdmin(ImportExportActionModelAdmin):
    resource_class = CompositionEquipmentResource
    list_display = ('equipment', 'thing', 'count')

@admin.register(StatusEquipment)
class StatusEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

@admin.register(Status)
class StatusAdmin(ImportExportActionModelAdmin):
    resource_class = StatusResource
    list_display = ('name', )



