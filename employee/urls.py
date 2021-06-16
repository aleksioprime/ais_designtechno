from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import UserEdit, EmployeeList, index, get_notebook, LogNoteBookList, FeedBackView

app_name = 'employee'

urlpatterns = [
    path('profile/<slug>', UserEdit.as_view(), name='user_edit'),
    path('', index, name='index'),
    path('employees/', EmployeeList.as_view(), name='users'),
    path('employees/notebook/<int:card>/<int:loc>', get_notebook, name='get_notebook'),
    path('employees/notebook/', LogNoteBookList.as_view(), name='log_notebook'),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)