from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import AdmissionApplication, StudentDocument

class StudentRegistrationForm(UserCreationForm):

    username = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
        label="Username"
    )

    email = forms.EmailField(required=True)

    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        label="Last Name"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()

        return user
class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['course', 'marks']

        labels = {
            'course': 'Select Course',
            'marks': 'Previous Academic Marks (%)',
        }

        widgets = {
            'course': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'marks': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter marks percentage',
                    'min': '0',
                    'max': '100',
                    'step': '0.01',
                }
            ),
        }
class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = [ 'student_name',
            'email',
            'document_type',
            'document_file',]

        widgets = {
            'application': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'document_type': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'document': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }
class StudentProfileForm(forms.ModelForm):

    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your address'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        }
