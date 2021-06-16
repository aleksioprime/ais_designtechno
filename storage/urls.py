from django.urls import path  
from django.conf.urls.static import static
from django.conf import settings
from .views import ThingList, ThingEdit, ThingDelete, ThingCreate, ThingDetail, UseThingEdit, \
    UseThingDelete, UseThingCreate, CompositionCreate, CompositionEdit, CompositionDelete, \
    StatusThingCreate, StatusThingEdit, StatusThingDelete

app_name = 'storage'

urlpatterns = [
    # пути для работы с материально-техническим обеспечением (оборудованием и материалами)
    path('storage/', ThingList.as_view(), name='index'),
    path('storage/thing/create/', ThingCreate.as_view(), name='thing_create'),
    path('storage/thing/<int:pk>/detail/', ThingDetail.as_view(), name='thing_detail'),
    path('storage/thing/<int:pk>/edit/', ThingEdit.as_view(), name='thing_edit'),
    path('storage/thing/<int:pk>/delete/', ThingDelete.as_view(), name='thing_delete'),

    # пути для работы с составом наборов
    path('storage/thing/<int:thing_pk>/composition/create/', CompositionCreate.as_view(), name='composition_create'),
    path('storage/thing/<int:thing_pk>/composition/<int:pk>/edit/', CompositionEdit.as_view(), name='composition_edit'),
    path('storage/thing/<int:thing_pk>/composition/<int:pk>/delete/', CompositionDelete.as_view(), name='composition_delete'),
    
    # пути для работы c использованием предметов
    path('storage/thing/<int:thing_pk>/usething/<int:pk>/edit/', UseThingEdit.as_view(), name='usething_edit'),
    path('storage/thing/<int:thing_pk>/usething/<int:pk>/delete/', UseThingDelete.as_view(), name='usething_delete'),
    path('storage/thing/<int:thing_pk>/usething/create/', UseThingCreate.as_view(), name='usething_create'),

    # пути для работы c присвоением статусов
    path('storage/thing/<int:thing_pk>/status/create/', StatusThingCreate.as_view(), name='statusthing_create'),
    path('storage/thing/<int:thing_pk>/status/<int:pk>/edit/', StatusThingEdit.as_view(), name='statusthing_edit'),
    path('storage/thing/<int:thing_pk>/status/<int:pk>/delete/', StatusThingDelete.as_view(), name='statusthing_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)