from django import forms
from django.contrib.auth.models import User
from .models import Task
from .models import UserProfile
from .models import Document

class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'category', 'file']


RELIGION_CHOICES = [
    ('Hindu', 'Hindu'),
    ('Muslim', 'Muslim'),
    ('Christian', 'Christian'),
    ('Sikh', 'Sikh'),
    ('Buddhist', 'Buddhist'),
    ('Jain', 'Jain'),
    ('Other', 'Other'),
]

CASTE_CHOICES = [
    ('General', 'General'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('Other', 'Other'),
]

INTEREST_CHOICES = [
    ('tech', 'Technology'),
    ('govt', 'Government Schemes'),
    ('exams', 'Competitive Exams'),
    ('health', 'Health & Wellness'),
    ('env', 'Environment'),
    ('startup', 'Startups'),
    ('finance', 'Finance & Taxes'),
    ('jobs', 'Job Updates'),
    ('edu', 'Higher Education'),
    ('scholarships', 'Scholarships'),
    ('welfare', 'Welfare'),
]
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    religion = forms.ChoiceField(choices=RELIGION_CHOICES)
    caste = forms.ChoiceField(choices=CASTE_CHOICES)
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['college', 'dob', 'education', 'income', 'location', 'religion', 'caste', 'interests','gender']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_interests(self):
        return ','.join(self.cleaned_data.get('interests', []))

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.interests:
            initial = kwargs.setdefault('initial', {})
            initial['interests'] = instance.interests.split(',')
        super().__init__(*args, **kwargs)



