from django.urls import path  
from django.conf.urls.static import static
from django.conf import settings
from .views import myp_subject_criteria
from .views import SubjectGroupView, CriteriaView, StrandView, ClassYearView, ObjectiveView, LevelView

app_name = 'sumassess'

urlpatterns = [
    # путь для работы с критериями и образовательными целями предметной области
    path('sumassess/criteria', myp_subject_criteria, name='criteria'),
    # адрес api для получения данных о предметных группах выбранной программы IB
    path('api/sumassess/subjectgroups', SubjectGroupView.as_view(), name='api_subjectgroups'),
    # адрес api для получения данных о критериях выбранной предметной группы
    path('api/sumassess/criteria', CriteriaView.as_view(), name='api_criteria'),
    # адрес api для получения данных о стрендах выбранной предметной группы
    path('api/sumassess/strands', StrandView.as_view(), name='api_strands'),
    # адрес api для получения данных о годах обучения выбранной программы IB
    path('api/sumassess/yearib', ClassYearView.as_view(), name='api_yearib'),
    # адрес api для получения данных об образовательных целях выбранного года и предметной группы или выбранного стрэнда
    path('api/sumassess/objectives', ObjectiveView.as_view(), name='api_objectives'),
    # адрес api для получения данных об уровнях достижений выбранного года и предметной группы или выбранного стрэнда
    path('api/sumassess/levels', LevelView.as_view(), name='api_levels'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)