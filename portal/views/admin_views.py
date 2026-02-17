from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ..models import (
    User, Student, Teacher, Class, Subject, Term, Result,
    Announcement, AdmissionApplication, ContactMessage,
    AcademicSession, ClassSubject,
)
from ..forms import AnnouncementForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_dashboard(request):
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()
    pending_results = Result.objects.filter(status=Result.STATUS_PENDING).count()
    pending_admissions = AdmissionApplication.objects.filter(status=AdmissionApplication.STATUS_PENDING).count()
    unread_contacts = ContactMessage.objects.filter(read=False).count()
    return render(request, 'portal/admin/dashboard.html', {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'pending_results': pending_results,
        'pending_admissions': pending_admissions,
        'unread_contacts': unread_contacts,
    })


@login_required
@admin_required
def student_management(request):
    students = Student.objects.select_related('user', 'current_class').all()
    return render(request, 'portal/admin/student_management.html', {'students': students})


@login_required
@admin_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    results = Result.objects.filter(student=student).select_related('subject', 'term').order_by('-term__start_date')
    return render(request, 'portal/admin/student_profile.html', {'student': student, 'results': results})


@login_required
@admin_required
def teacher_management(request):
    teachers = Teacher.objects.select_related('user').prefetch_related('subjects').all()
    return render(request, 'portal/admin/teacher_management.html', {'teachers': teachers})


@login_required
@admin_required
def teacher_profile(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    assigned = ClassSubject.objects.filter(teacher=teacher).select_related('class_ref', 'subject')
    return render(request, 'portal/admin/teacher_profile.html', {'teacher': teacher, 'assigned': assigned})


@login_required
@admin_required
def class_management(request):
    classes = Class.objects.prefetch_related('class_subjects__subject', 'class_subjects__teacher').all()
    subjects = Subject.objects.all()
    return render(request, 'portal/admin/class_management.html', {'classes': classes, 'subjects': subjects})


@login_required
@admin_required
def results_management(request):
    pending = Result.objects.filter(status=Result.STATUS_PENDING).select_related('student__user', 'subject', 'term', 'uploaded_by')
    return render(request, 'portal/admin/results_management.html', {'pending_results': pending})


@login_required
@admin_required
def approve_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    result.status = Result.STATUS_APPROVED
    result.approved_at = timezone.now()
    result.save()
    messages.success(request, 'Result approved. It is now visible to the student.')
    return redirect('portal:results_management')


@login_required
@admin_required
def reject_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    result.status = Result.STATUS_REJECTED
    result.save()
    messages.info(request, 'Result rejected.')
    return redirect('portal:results_management')


@login_required
@admin_required
def announcements_list(request):
    announcements = Announcement.objects.select_related('target_class', 'created_by').order_by('-date')[:50]
    return render(request, 'portal/admin/announcements.html', {'announcements': announcements})


@login_required
@admin_required
def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, 'Announcement added.')
            return redirect('portal:announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'portal/admin/add_announcement.html', {'form': form})


@login_required
@admin_required
def admissions_queue(request):
    applications = AdmissionApplication.objects.select_related('applying_class').filter(
        status=AdmissionApplication.STATUS_PENDING
    ).order_by('-submitted_at')
    return render(request, 'portal/admin/admissions_queue.html', {'applications': applications})


@login_required
@admin_required
def approve_admission(request, pk):
    app = get_object_or_404(AdmissionApplication, pk=pk)
    app.status = AdmissionApplication.STATUS_APPROVED
    app.reviewed_by = request.user
    app.reviewed_at = timezone.now()
    app.save()
    messages.success(request, 'Application approved. You can now create a student record from the admin.')
    return redirect('portal:admissions_queue')


@login_required
@admin_required
def reject_admission(request, pk):
    app = get_object_or_404(AdmissionApplication, pk=pk)
    app.status = AdmissionApplication.STATUS_REJECTED
    app.reviewed_by = request.user
    app.reviewed_at = timezone.now()
    app.save()
    messages.info(request, 'Application rejected.')
    return redirect('portal:admissions_queue')


@login_required
@admin_required
def settings_page(request):
    sessions = AcademicSession.objects.all()
    return render(request, 'portal/admin/settings.html', {'sessions': sessions})
