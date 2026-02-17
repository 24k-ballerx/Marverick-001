from .auth import login_view, logout_view
from .dashboard import dashboard
from .admin_views import (
    admin_dashboard, student_management, teacher_management,
    class_management, results_management, announcements_list, add_announcement,
    admissions_queue, settings_page,
    student_profile, teacher_profile,
    approve_result, reject_result,
    approve_admission, reject_admission,
)
from .teacher_views import teacher_dashboard, upload_results, view_students
from .student_views import student_dashboard, my_results, student_announcements

__all__ = [
    'login_view', 'logout_view', 'dashboard',
    'admin_dashboard', 'student_management', 'teacher_management',
    'class_management', 'results_management', 'announcements_list', 'add_announcement',
    'admissions_queue', 'settings_page',
    'student_profile', 'teacher_profile',
    'approve_result', 'reject_result', 'approve_admission', 'reject_admission',
    'teacher_dashboard', 'upload_results', 'view_students',
    'student_dashboard', 'my_results', 'student_announcements',
]
