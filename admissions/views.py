from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from .forms import (
    StudentRegistrationForm,
    AdmissionApplicationForm,
    StudentDocumentForm,
    StudentProfileForm,

)

from .models import (
    Course,
    AdmissionApplication,
    StudentDocument,
    StudentProfile,
)


# Home Page
def home(request):
    return render(request, 'admissions/home.html')


# Courses Page
def courses(request):
    all_courses = Course.objects.all()

    return render(
        request,
        'admissions/courses.html',
        {'courses': all_courses}
    )


# Student Registration
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Registration successful!'
            )

            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'admissions/register.html',
        {'form': form}
    )


# Student Login
def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(
        request,
        'admissions/login.html',
        {'form': form}
    )


# Student Logout
def student_logout(request):
    logout(request)

    messages.success(
        request,
        'You have logged out successfully!'
    )

    return redirect('login')


# Student Dashboard
@login_required(login_url='login')
def dashboard(request):
    applications = AdmissionApplication.objects.filter(
        student=request.user
    ).select_related(
        'course'
    ).order_by('-application_date')

    documents = StudentDocument.objects.filter(
        application__student=request.user
    ).select_related(
        'application',
        'application__course'
    )

    context = {
        'applications': applications,
        'documents': documents,
    }

    return render(
        request,
        'admissions/dashboard.html',
        context
    )


@login_required(login_url='login')
def apply_admission(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()

            messages.success(
                request,
                'Admission application submitted successfully!'
            )

            return redirect('dashboard')
    else:
        form = AdmissionApplicationForm()

    return render(
        request,
        'admissions/apply_admission.html',
        {'form': form}
    )
# Upload Documents
@login_required(login_url='login')
def upload_document(request):
    applications = AdmissionApplication.objects.filter(
        student=request.user
    )

    if request.method == 'POST':
        form = StudentDocumentForm(
            request.POST,
            request.FILES
        )

        form.fields['application'].queryset = applications

        if form.is_valid():
            document = form.save(commit=False)
            document.save()

            messages.success(
                request,
                'Document uploaded successfully!'
            )

            return redirect('dashboard')

    else:
        form = StudentDocumentForm()
        form.fields['application'].queryset = applications

    return render(
        request,
        'admissions/upload_document.html',
        {'form': form}
    )


# Admin Dashboard
@staff_member_required(login_url='login')
def admin_dashboard(request):
    total_students = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).count()

    total_applications = AdmissionApplication.objects.count()

    approved_applications = AdmissionApplication.objects.filter(
        status='Approved'
    ).count()

    pending_applications = AdmissionApplication.objects.filter(
        status='Pending'
    ).count()

    rejected_applications = AdmissionApplication.objects.filter(
        status='Rejected'
    ).count()

    total_courses = Course.objects.count()

    total_documents = StudentDocument.objects.count()

    verified_documents = StudentDocument.objects.filter(
        verified=True
    ).count()

    context = {
        'total_students': total_students,
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
        'rejected_applications': rejected_applications,
        'total_courses': total_courses,
        'total_documents': total_documents,
        'verified_documents': verified_documents,
    }

    return render(
        request,
        'admissions/admin_dashboard.html',
        context
    )


# Student Profile
@login_required(login_url='login')
def student_profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'address': '',
        }
    )

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            profile.phone = form.cleaned_data['phone']
            profile.address = form.cleaned_data['address']
            profile.save()

            messages.success(
                request,
                'Your profile was updated successfully!'
            )

            return redirect('student_profile')

    else:
        form = StudentProfileForm(
            instance=request.user,
            initial={
                'phone': profile.phone,
                'address': profile.address,
            }
        )

    return render(
        request,
        'admissions/profile.html',
        {
            'form': form,
            'profile': profile,
        }
    )