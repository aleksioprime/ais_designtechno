from django.urls import path  
from django.conf.urls.static import static
from django.conf import settings
from .views import ThingList, ThingDetail, ThingEdit, ThingDelete, ThingCreate, UseThingsEdit,UseThingsCreate, UseThingsDelete

app_name = 'storage'

urlpatterns = [
    path('storage/', ThingList.as_view(), name='things'),
    path('storage/<int:pk>/', ThingDetail.as_view(), name='things_detail'),
    path('storage/<int:pk>/edit/', ThingEdit.as_view(), name='things_edit'),
    path('storage/<int:pk>/delete/', ThingDelete.as_view(), name='things_delete'),
    path('storage/create/', ThingCreate.as_view(), name='things_create'),
    path('storage/usethings/<slug>/edit/', UseThingsEdit.as_view(), name='usethings_edit'),
    path('storage/usethings/<int:pk>/delete/', UseThingsDelete.as_view(), name='usethings_delete'),
    path('storage/usethings/create/', UseThingsCreate.as_view(), name='usethings_create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)