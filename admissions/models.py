from django.db import models
from django.contrib.auth.models import User


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
class StudentDocument(models.Model):

    DOCUMENT_TYPES = [
        ('Aadhaar', 'Aadhaar Card'),
        ('Marksheet', 'Marksheet'),
        ('Photo', 'Passport Photo'),
        ('Other', 'Other'),
    ]

    application = models.ForeignKey(
        AdmissionApplication,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES
    )
    document = models.FileField(
        upload_to='documents/'
    )
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.document_type
