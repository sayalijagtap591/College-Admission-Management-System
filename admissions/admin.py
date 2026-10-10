from django.contrib import admin
from .models import (
    Course,
    StudentProfile,
    AdmissionApplication,
    StudentDocument
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_name',
        'course_code',
        'duration',
        'fees'
    )

    search_fields = (
        'course_name',
        'course_code'
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'date_of_birth'
    )

    search_fields = (
        'user__username',
        'user__first_name'
    )


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'marks',
        'status',
        'application_date'
    )

    list_filter = (
        'status',
        'course'
    )

    search_fields = (
        'student__username',
        'course__course_name'
    )

    list_editable = ('status',)


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'application',
        'document_type',
        'verified'
    )

    list_filter = (
        'document_type',
        'verified'
    )

    list_editable = ('verified',)