from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', views.home, name='home'),
path('courses/', views.courses, name='courses'),
path('register/', views.register, name='register'),
path('login/', views.student_login, name='login'),
path(
        'logout/',
        views.student_logout,
        name='student_logout'
    ),

path('dashboard/', views.dashboard, name='dashboard'),
path(
    'apply-admission/',
    views.apply_admission,
    name='apply_admission'
),
path(
    'upload-document/',
    views.upload_document,
    name='upload_document'
),
path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),

path('profile/', views.student_profile, name='student_profile'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
