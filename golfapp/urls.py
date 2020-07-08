from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpView, HomeView
from .views import CourseList, CourseCreate, CourseDelete, CourseUpdate, CourseDetail, CoursePictureCreate, CoursePictureDetail, CoursePictureDelete
from .views import TeeColorCreate
from .views import HoleCreate, HoleDelete
from .views import TeeCreate, TeeDelete, TeeUpdate
from .views import RoundCreate, RoundDetail, RoundUpdate, RoundDelete
from .views import ScoreCreate

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('signup/', SignUpView.as_view(), name='signup'),

    path('courses/', CourseList.as_view(), name='course_list'),
    path('course/create', CourseCreate.as_view(), name='course_create'),
    path('courses/delete/<int:pk>', CourseDelete.as_view(), name='course_delete'),
    path('courses/update/<int:pk>', CourseUpdate.as_view(), name='course_update'),
    path('course/<int:pk>', CourseDetail.as_view(), name='course_detail'),

    url(r'courses/(?P<course_pk>\w+)/teecolor/create', TeeColorCreate.as_view(), name='teecolor_create'),

    url(r'courses/(?P<course_pk>\w+)/hole/create', HoleCreate.as_view(), name='hole_create'),
    url(r'courses/(?P<course_pk>\w+)/holes/delete/(?P<pk>\w+)', HoleDelete.as_view(), name='hole_delete'),

    url(r'course/(?P<course_pk>\w+)/hole/(?P<hole_pk>\w+)/tee/create/', TeeCreate.as_view(), name='tee_create'),
    url(r'course/(?P<course_pk>\w+)/hole/(?P<hole_pk>\w+)/tee/update/(?P<pk>\w+)', TeeUpdate.as_view(), name='tee_update'),
    url(r'courses/(?P<course_pk>\w+)/hole/(?P<hole_pk>\w+)/tees/delete/(?P<pk>\w+)', TeeDelete.as_view(), name='tee_delete'),

    path('round/create', RoundCreate.as_view(), name='round_create'),
    path('round/<int:pk>', RoundDetail.as_view(), name='round_detail'),
    path('rounds/update/<int:pk>', RoundUpdate.as_view(), name='round_update'),
    path('rounds/delete/<int:pk>', RoundDelete.as_view(), name='round_delete'),

    url(r'round/(?P<round_pk>\w+)/hole/(?P<hole_pk>\w+)/score/create/', ScoreCreate.as_view(), name='score_create'),

    url(r'courses/(?P<course_pk>\w+)/coursepicture/create', CoursePictureCreate.as_view(), name='coursepicture_create'),
    url(r'courses/(?P<course_pk>\w+)/coursepicture/(?P<pk>\w+)', CoursePictureDetail.as_view(), name='coursepicture_detail'),
    url(r'courses/(?P<course_pk>\w+)/coursepictures/delete/(?P<pk>\w+)', CoursePictureDelete.as_view(), name='coursepicture_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)