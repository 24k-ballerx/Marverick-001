from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
from ..models import Student, Result, Announcement, Term


def _greeting():
    h = datetime.now().hour
    if h < 12:
        return 'Morning'
    if h < 17:
        return 'Afternoon'
    return 'Evening'


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@student_required
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None
    # School-wide + class-specific announcements
    announcements = Announcement.objects.filter(
        Q(scope=Announcement.SCOPE_SCHOOL) | (Q(target_class=student.current_class) if student and student.current_class else Q(pk__in=[]))
    ).distinct().order_by('-date')[:10]
    return render(request, 'portal/student/dashboard.html', {
        'student': student,
        'announcements': announcements,
        'greeting': _greeting(),
    })


@login_required
@student_required
def my_results(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None
    term_pk = request.GET.get('term')
    results = []
    terms = Term.objects.select_related('session').order_by('-session__start_date', '-start_date')
    if student and term_pk:
        results = Result.objects.filter(
            student=student,
            term_id=term_pk,
            status=Result.STATUS_APPROVED
        ).select_related('subject', 'term')
    elif student:
        results = Result.objects.filter(
            student=student,
            status=Result.STATUS_APPROVED
        ).select_related('subject', 'term').order_by('-term__start_date')
    return render(request, 'portal/student/my_results.html', {
        'student': student,
        'results': results,
        'terms': terms,
        'selected_term': term_pk,
    })


@login_required
@student_required
def student_announcements(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None
    announcements = Announcement.objects.filter(
        Q(scope=Announcement.SCOPE_SCHOOL) | (Q(target_class=student.current_class) if student and student.current_class else Q(pk__in=[]))
    ).distinct().order_by('-date')
    return render(request, 'portal/student/announcements.html', {'announcements': announcements, 'student': student})
