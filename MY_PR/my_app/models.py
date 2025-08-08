from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTP(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} on {self.date}"


class Exam(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    type = models.CharField(max_length=100, default='Government')  # <-- Add default
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Scheme(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)

    EDUCATION_CHOICES = [
        ('High School', 'High School'),
        ('Diploma', 'Diploma'),
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('PhD', 'PhD'),
    ]
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, blank=True)

    INCOME_CHOICES = [
        ('<1 Lakh', '<1 Lakh'),
        ('1-3 Lakhs', '1-3 Lakhs'),
        ('3-5 Lakhs', '3-5 Lakhs'),
        ('5-10 Lakhs', '5-10 Lakhs'),
        ('>10 Lakhs', '>10 Lakhs'),
    ]
    income = models.CharField(max_length=20, choices=INCOME_CHOICES, blank=True)

    location = models.CharField(max_length=100, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True)  # Store as comma-separated string

    def __str__(self):
        return self.user.username
