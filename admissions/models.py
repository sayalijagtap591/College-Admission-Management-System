from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. Course Management
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    duration = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.course_name


# 2. Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# 3. Admission Application
class AdmissionApplication(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    application_date = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"


# 4. Document Upload

class Admission(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.full_name    
class StudentDocument(models.Model):
    DOCUMENT_CHOICES = [
        ('Aadhaar Card', 'Aadhaar Card'),
        ('10th Marksheet', '10th Marksheet'),
        ('12th Marksheet', '12th Marksheet'),
        ('Leaving Certificate', 'Leaving Certificate'),
        ('Caste Certificate', 'Caste Certificate'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    student_name = models.CharField(
    max_length=100,
    blank=True,
    default=''
)

    email = models.EmailField(
    blank=True,
    default=''
)
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_CHOICES
    )
    document_file = models.FileField(
    upload_to='student_documents/',
    blank=True,
    null=True
)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.student_name} - {self.document_type}"