from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
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
from .models import Admission,StudentDocument


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


def admission_form(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course = request.POST.get("course")

        Admission.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            course=course
        )

        return render(request, "admissions/admission_form.html", {
            "success": True,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "course": course,
        })

    return render(request, "admissions/admission_form.html")
#Apply for Admission

@login_required(login_url='login')
def apply_admission(request):
    applications = AdmissionApplication.objects.filter(
    student=request.user
    )

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
    {
        'form': form,
        'applications': applications,
    }
)

# Student Dashboard
@login_required(login_url='login')
def dashboard(request):
    applications = AdmissionApplication.objects.filter(
        student=request.user
        ).select_related('course').order_by('-application_date')

    documents = StudentDocument.objects.all().order_by('-uploaded_at')

    context = {
        'applications': applications,
        'documents': documents,
        }

    return render(request, 'admissions/dashboard.html', context)

#  Upload Documents
@login_required(login_url='login')
def upload_document(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        document_type = request.POST.get('document_type')
        document_file = request.FILES.get('document_file')

        if document_file:
            StudentDocument.objects.create(
                student_name=student_name or request.user.username,
                email=email or request.user.email,
                document_type=document_type,
                document_file=document_file,
                status='Pending'
            )

            messages.success(request, 'Document uploaded successfully!')
            return redirect('dashboard')

        messages.error(request, 'Please select a document to upload.')

    return render(request, 'admissions/upload_document.html')

# Admin Dashboard
def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
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
        status='Verified'
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
@login_required
def merit_list(request):
    applications = AdmissionApplication.objects.select_related(
        'student', 'course'
    ).order_by('-marks')

    return render(
        request,
        'admissions/merit_list.html',
        {'applications': applications}
    )
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff, login_url='login')
def manage_applications(request):
    applications = AdmissionApplication.objects.select_related(
        'student', 'course'
    ).order_by('-application_date')

    context = {
        'applications': applications,
    }

    return render(
        request,
        'admissions/manage_applications.html',
        context
    )
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff, login_url='login')
@require_POST
def update_application_status(request, application_id):

    application = get_object_or_404(
        AdmissionApplication,
        id=application_id
    )

    new_status = request.POST.get('status')

    allowed_statuses = ['Approved', 'Rejected']

    if new_status not in allowed_statuses:
        messages.error(request, 'Invalid application status.')
        return redirect('manage_applications')

    if application.status != 'Pending':
        messages.warning(
            request,
            'Only pending applications can be updated.'
        )
        return redirect('manage_applications')

    application.status = new_status
    application.save(update_fields=['status'])

    messages.success(
        request,
        f'Application #{application.id} has been {new_status.lower()}.'
    )

    return redirect('manage_applications')
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff, login_url='login')
@require_POST
def update_document_status(request, document_id):
    document = get_object_or_404(StudentDocument, id=document_id)

    new_status = request.POST.get('status')

    if new_status not in ['Verified', 'Rejected']:
        messages.error(request, 'Invalid document status.')
        return redirect('manage_documents')

    if document.status != 'Pending':
        messages.warning(request, 'Only pending documents can be updated.')
        return redirect('manage_documents')

    document.status = new_status
    document.save(update_fields=['status'])

    messages.success(
        request,
        f'Document status updated to {new_status}.'
    )

    return redirect('manage_documents')
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff, login_url='login')
def manage_documents(request):
    documents = StudentDocument.objects.all().order_by('-uploaded_at')

    context = {
        'documents': documents
    }

    return render(request, 'admissions/manage_documents.html', context)