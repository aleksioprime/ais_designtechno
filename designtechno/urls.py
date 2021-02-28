from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('employee.urls')),
    path('', include('storage.urls')),
    path('', include('sumassess.urls')),
]

