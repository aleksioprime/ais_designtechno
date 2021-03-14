from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('employee.urls')),
    path('', include('storage.urls')),
    path('', include('sumassess.urls')),
]

# добавление панели DEBUG на всех страницах
# if settings.DEBUG:
#     import debug_toolbar

#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns