"""
URL configuration for medhashaala_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.auth import EmailTokenObtainView

# Import viewsets from apps
from users.views import UserViewSet
from students.views import StudentViewSet
from teachers.views import TeacherViewSet
from courses.views import AcademicYearViewSet, ClassViewSet, SubjectViewSet, ClassSubjectViewSet, SectionListView
from attendance.views import AttendanceViewSet
from grades.views import ExamTypeViewSet, ExamViewSet, GradeViewSet

# Configure the router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'class-subjects', ClassSubjectViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'exam-types', ExamTypeViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/sections/', SectionListView.as_view(), name='sections-list'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', EmailTokenObtainView.as_view(), name='api_token_auth'),
]
