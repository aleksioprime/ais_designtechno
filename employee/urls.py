from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import UserEdit, EmployeeList, index

app_name = 'employee'

urlpatterns = [
    path('profile/<slug>', UserEdit.as_view(), name='user_edit'),
    path('', index, name='index'),
    path('employees/', EmployeeList.as_view(), name='users'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)