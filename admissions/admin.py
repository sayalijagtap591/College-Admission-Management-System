from django.contrib import admin
from .models import (
    Course,
    StudentProfile,
    AdmissionApplication,
    Admission,
    StudentDocument,
)


# ==========================================
# COURSE ADMIN
# ==========================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'course_name',
        'course_code',
        'duration',
        'fees',
    )

    search_fields = (
        'course_name',
        'course_code',
    )

    list_filter = (
        'duration',
    )

    ordering = ('course_name',)


# ==========================================
# STUDENT PROFILE ADMIN
# ==========================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'phone',
        'date_of_birth',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )

    ordering = ('id',)


# ==========================================
# ADMISSION APPLICATION ADMIN
# ==========================================

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'course',
        'marks',
        'status',
        'application_date',
    )

    list_filter = (
        'status',
        'course',
        'application_date',
    )

    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'course__course_name',
    )

    list_editable = (
        'status',
    )

    ordering = ('-application_date',)


# ==========================================
# ADMISSION ADMIN
# ==========================================

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'full_name',
        'email',
        'phone',
        'course',
        'created_at',
    )

    search_fields = (
        'full_name',
        'email',
        'phone',
    )

    list_filter = (
        'course',
        'created_at',
    )

    ordering = ('-created_at',)


# ==========================================
# STUDENT DOCUMENT VERIFICATION ADMIN
# ==========================================

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student_name',
        'email',
        'document_type',
        'document_file',
        'status',
        'uploaded_at',
    )

    list_filter = (
        'status',
        'document_type',
        'uploaded_at',
    )

    search_fields = (
        'student_name',
        'email',
    )

    list_editable = (
        'status',
    )

    ordering = ('-uploaded_at',)

    readonly_fields = (
        'uploaded_at',
    )
