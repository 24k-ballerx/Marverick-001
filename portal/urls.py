from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/students/', views.student_management, name='student_management'),
    path('admin/students/<int:pk>/', views.student_profile, name='student_profile'),
    path('admin/teachers/', views.teacher_management, name='teacher_management'),
    path('admin/teachers/<int:pk>/', views.teacher_profile, name='teacher_profile'),
    path('admin/classes/', views.class_management, name='class_management'),
    path('admin/results/', views.results_management, name='results_management'),
    path('admin/results/<int:pk>/approve/', views.approve_result, name='approve_result'),
    path('admin/results/<int:pk>/reject/', views.reject_result, name='reject_result'),
    path('admin/announcements/', views.announcements_list, name='announcements_list'),
    path('admin/announcements/add/', views.add_announcement, name='add_announcement'),
    path('admin/admissions/', views.admissions_queue, name='admissions_queue'),
    path('admin/admissions/<int:pk>/approve/', views.approve_admission, name='approve_admission'),
    path('admin/admissions/<int:pk>/reject/', views.reject_admission, name='reject_admission'),
    path('admin/settings/', views.settings_page, name='settings'),

    # Teacher
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/upload-results/', views.upload_results, name='upload_results'),
    path('teacher/students/', views.view_students, name='view_students'),

    # Student
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/results/', views.my_results, name='my_results'),
    path('student/announcements/', views.student_announcements, name='student_announcements'),
]
