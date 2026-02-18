from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, AcademicSession, Term, Class, Subject,
    Teacher, Student, ClassSubject, Result, Announcement,
    AdmissionApplication, ContactMessage, NewsArticle, Attendance,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + [('Portal', {'fields': ('role', 'phone', 'avatar')})]
    add_fieldsets = BaseUserAdmin.add_fieldsets + [('Portal', {'fields': ('role', 'phone')})]


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'start_date', 'end_date')
    list_filter = ('session',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id')
    filter_horizontal = ('subjects',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'current_class', 'parent_contact')
    list_filter = ('current_class',)


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_ref', 'subject', 'teacher')
    list_filter = ('class_ref',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'score', 'status', 'uploaded_by', 'created_at')
    list_filter = ('term', 'status', 'subject')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'scope', 'target_class', 'created_by')
    list_filter = ('scope', 'date')


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'applying_class', 'status', 'submitted_at')
    list_filter = ('status', 'applying_class')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'read', 'submitted_at')
    list_filter = ('read',)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present', 'remarks')
    list_filter = ('date', 'present')
