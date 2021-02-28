from django.urls import path  
from django.conf.urls.static import static
from django.conf import settings
from sumassess.views import criteria_page,\
    CriteriaView, ObjectiveView, YearIBView, UnitList, AssessmentUnitView, unit_assessment_page, StudentView,\
        AssessmentUnitList, UnitView, GroupView, AssessmentUnitDelete, LevelView, UnitDelete, UnitCreate, UnitEdit, UnitDetail


app_name = 'sumassess'

urlpatterns = [
    path('sumassess/criteria/', criteria_page, name='criteria'),
    path('api/objective/', ObjectiveView.as_view(), name='api_obj'),
    path('api/criteria/', CriteriaView.as_view(), name='api_cri'),
    path('api/yearib/', YearIBView.as_view(), name='api_year'),
    path('sumassess/', UnitList.as_view(), name='index'),
    path('sumassess/unit/create/', UnitCreate.as_view(), name='unit_create'),
    path('sumassess/unit/detail/<int:pk>', UnitDetail.as_view(), name='unit_detail'),
    path('sumassess/unit/edit/<int:pk>', UnitEdit.as_view(), name='unit_edit'),
    path('sumassess/unit/delete/<int:pk>', UnitDelete.as_view(), name='unit_delete'),
    path('sumassess/students/', AssessmentUnitList.as_view(), name='students'),
    path('sumassess/students/delete/<int:pk>', AssessmentUnitDelete.as_view(), name='student_delete'),
    # path('sumassess/students/edit/<int:pk>', AssessmentUnitEdit.as_view(), name='student_edit'),
    path('api/unit/<int:pk>', UnitView.as_view(), name='api_unit'),
    path('api/assessmentunit/<int:pk>', AssessmentUnitView.as_view(), name='api_assessmentunit'),
    path('api/student/', StudentView.as_view(), name='api_student'),
    path('api/group/', GroupView.as_view(), name='api_group'),
    path('api/levels/', LevelView.as_view(), name='api_level'),
    path('sumassess/student/assessment/<int:id_assessstudent>/<int:id_year>/<int:id_unit>', unit_assessment_page, name='assessment'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)