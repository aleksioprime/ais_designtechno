from django.contrib import admin
from storage.models import Thing, UseThing, Composition, Cabinet, Status, StatusThing
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

# класс ресурса для создания импорта-экспорта таблицы Thing
class ThingResource(resources.ModelResource):
    class Meta:
        model = Thing

# класс ресурса для создания импорта-экспорта таблицы UseThing
class UseThingResource(resources.ModelResource):
    class Meta:
        model = UseThing

# класс ресурса для создания импорта-экспорта таблицы Cabinet
class CabinetResource(resources.ModelResource):
    class Meta:
        model = Cabinet

# класс ресурса для создания импорта-экспорта таблицы Composition
class CompositionResource(resources.ModelResource):
    class Meta:
        model = Composition

# класс ресурса для создания импорта-экспорта таблицы Status
class StatusResource(resources.ModelResource):
    class Meta:
        model = Status

# класс ресурса для создания импорта-экспорта таблицы StatusThing
class StatusThingResource(resources.ModelResource):
    class Meta:
        model = StatusThing

# класс модели Thing
@admin.register(Thing)
class ThingAdmin(ImportExportActionModelAdmin):
    resource_class = ThingResource
    list_display = ['name', 'name_docs', 'count']

# класс модели UseThing
@admin.register(UseThing)
class UseThingAdmin(ImportExportActionModelAdmin):
    resource_class = UseThingResource
    list_display = ('thing', 'employee', 'count')

# класс модели Cabinet
@admin.register(Cabinet)
class CabinetAdmin(ImportExportActionModelAdmin):
    resource_class = CabinetResource
    list_display = ('label', 'name')

# класс модели Equipment
@admin.register(Composition)
class CompositionAdmin(ImportExportActionModelAdmin):
    resource_class = CompositionResource
    list_display = ('thing', 'equipment', 'count')

# класс модели Status
@admin.register(Status)
class StatusAdmin(ImportExportActionModelAdmin):
    resource_class = StatusResource
    list_display = ('name', )

# класс модели StatusThing
@admin.register(StatusThing)
class StatusThingAdmin(ImportExportActionModelAdmin):
    resource_class = StatusThingResource
    list_display = ('thing', 'status', 'count', 'update')



