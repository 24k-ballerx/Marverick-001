from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from ..models import Teacher, Student, Class, Subject, Term, Result, Announcement, ClassSubject


def _greeting():
    h = datetime.now().hour
    if h < 12:
        return 'Morning'
    if h < 17:
        return 'Afternoon'
    return 'Evening'


def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@teacher_required
def teacher_dashboard(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        teacher = None
    my_classes = ClassSubject.objects.filter(teacher=teacher).select_related('class_ref', 'subject') if teacher else []
    announcements = Announcement.objects.filter(scope=Announcement.SCOPE_SCHOOL).order_by('-date')[:10]
    pending_count = Result.objects.filter(uploaded_by=request.user, status=Result.STATUS_PENDING).count()
    return render(request, 'portal/teacher/dashboard.html', {
        'teacher': teacher,
        'my_classes': my_classes,
        'announcements': announcements,
        'pending_count': pending_count,
        'greeting': _greeting(),
    })


@login_required
@teacher_required
def upload_results(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        teacher = None
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    terms = Term.objects.select_related('session').order_by('-session__start_date', '-start_date')[:10]
    # Show results table for selected class
    class_pk = request.GET.get('class')
    subject_pk = request.GET.get('subject')
    term_pk = request.GET.get('term')
    students = []
    if class_pk and term_pk:
        term = get_object_or_404(Term, pk=term_pk)
        cls = get_object_or_404(Class, pk=class_pk)
        students = Student.objects.filter(current_class=cls).select_related('user')
    return render(request, 'portal/teacher/upload_results.html', {
        'classes': classes,
        'subjects': subjects,
        'terms': terms,
        'students': students,
        'selected_class': class_pk,
        'selected_subject': subject_pk,
        'selected_term': term_pk,
    })


@login_required
@teacher_required
def view_students(request):
    class_pk = request.GET.get('class')
    students = []
    cls = None
    if class_pk:
        cls = get_object_or_404(Class, pk=class_pk)
        students = Student.objects.filter(current_class=cls).select_related('user')
    classes = Class.objects.all()
    return render(request, 'portal/teacher/view_students.html', {
        'classes': classes,
        'students': students,
        'selected_class': cls,
    })
