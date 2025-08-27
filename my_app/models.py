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


# -------------------- EXAM MODEL --------------------
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('State Level', 'State Level'),
        ('National Level', 'National Level'),
        ('University Level', 'University Level'),  # Added to match seed data
    ]

    LOCATION_CHOICES = [
        ('Delhi', 'Delhi'),
        ('Bengaluru', 'Bengaluru'),
        ('Mumbai', 'Mumbai'),
        ('West Bengal', 'West Bengal'),
        ('Hyderabad', 'Hyderabad'),
        ('Chennai', 'Chennai'),
        ('Pune', 'Pune'),
        ('Kolkata', 'Kolkata'),
        ('Lucknow', 'Lucknow'),
        ('All India', 'All India'),
        ('Multiple Cities', 'Multiple Cities'),  # Added to match seed data
        ('Karnataka', 'Karnataka'),  # Added to match seed data
        ('Maharashtra', 'Maharashtra'),  # Added to match seed data
        ('Telangana', 'Telangana'),  # Added to match seed data
        ('Andhra Pradesh', 'Andhra Pradesh'),  # Added to match seed data
        ('Odisha', 'Odisha'),  # Added to match seed data
        ('Gujarat', 'Gujarat'),  # Added to match seed data
        ('Chhattisgarh', 'Chhattisgarh'),  # Added to match seed data
        ('Madhya Pradesh', 'Madhya Pradesh'),  # Added to match seed data
        ('Tamil Nadu', 'Tamil Nadu'),  # Added to match seed data
        ('Uttarakhand', 'Uttarakhand'),  # Added to match seed data
        ('Kerala', 'Kerala'),  # Added to match seed data
        ('Bhubaneswar', 'Bhubaneswar'),  # Added to match seed data
        ('Vellore', 'Vellore'),  # Added to match seed data
        ('Ahmedabad', 'Ahmedabad'),  # Added to match seed data
        ('Rural India', 'Rural India'),  # Added to match seed data
    ]

    CATEGORY_CHOICES = [
        ('Engineering', 'Engineering'),
        ('Medical', 'Medical'),
        ('Banking', 'Banking'),
        ('Defense', 'Defense'),
        ('Civil Services', 'Civil Services'),
        ('Teaching', 'Teaching'),
        ('Law', 'Law'),
        ('Management', 'Management'),
        ('Science', 'Science'),  # Added to match seed data
        ('Design', 'Design'),  # Added to match seed data
        ('Employment', 'Employment'),  # Added to match seed data
        ('Insurance', 'Insurance'),  # Added to match seed data
        ('Food Corporation', 'Food Corporation'),  # Added to match seed data
        ('Agriculture', 'Agriculture'),  # Added to match seed data
        ('Hotel Management', 'Hotel Management'),  # Added to match seed data
    ]

    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Both', 'Both'),
    ]

    name = models.CharField(max_length=255, unique=True)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES, default="Government")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Engineering")
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default="All India")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default="Offline")
    date = models.DateField(blank=True, null=True) # Single date field to match seed data

    def __str__(self):
        return self.name


# -------------------- SCHEME MODEL --------------------
class Scheme(models.Model):
    SCHEME_TYPE_CHOICES = [
        ('Central Government', 'Central Government'),
        ('State Government', 'State Government'),
        ('Welfare', 'Welfare'),
        ('Scholarship', 'Scholarship'),
        ('Loan', 'Loan'),
        ('Employment', 'Employment'),
        ('Training', 'Training'),  # Added to match seed data
        ('Pension', 'Pension'),  # Added to match seed data
        ('Insurance', 'Insurance'),  # Added to match seed data
        ('Financial Assistance', 'Financial Assistance'),  # Added to match seed data
        ('Subsidy', 'Subsidy'),  # Added to match seed data
        ('Allowance', 'Allowance'),  # Added to match seed data
    ]

    ELIGIBILITY_CHOICES = [
        ('10th Pass', '10th Pass'),
        ('12th Pass', '12th Pass'),
        ('Graduate', 'Graduate'),
        ('Postgraduate', 'Postgraduate'),
        ('Open to All', 'Open to All'),
        ('18+ years', '18+ years'),  # Added to match seed data
        ('18-50 years', '18-50 years'),  # Added to match seed data
        ('18-70 years', '18-70 years'),  # Added to match seed data
        ('18-40 years', '18-40 years'),  # Added to match seed data
        ('Senior Citizens', 'Senior Citizens'),  # Added to match seed data
        ('BPL Families', 'BPL Families'),  # Added to match seed data
        ('SC/ST/Women', 'SC/ST/Women'),  # Added to match seed data
        ('Rural Population', 'Rural Population'),  # Added to match seed data
        ('Farmers', 'Farmers'),  # Added to match seed data
        ('State Residents', 'State Residents'),  # Added to match seed data
        ('Girl Students', 'Girl Students'),  # Added to match seed data
        ('Girls from BPL families', 'Girls from BPL families'),  # Added to match seed data
        ('Graduate, Unemployed', 'Graduate, Unemployed'),  # Added to match seed data
        ('All Residents', 'All Residents'),  # Added to match seed data
        ('Startups registered in Delhi', 'Startups registered in Delhi'),  # Added to match seed data
        ('Low Income', 'Low Income'),  # Added to match seed data
    ]

    CATEGORY_CHOICES = [
        ('Education', 'Education'),
        ('Employment', 'Employment'),
        ('Health', 'Health'),
        ('Finance', 'Finance'),
        ('General', 'General'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Housing', 'Housing'),  # Added to match seed data
        ('Welfare', 'Welfare'),  # Added to match seed data
        ('Insurance', 'Insurance'),  # Added to match seed data
        ('Pension', 'Pension'),  # Added to match seed data
        ('Food Corporation', 'Food Corporation'),  # Added to match seed data
    ]

    LOCATION_CHOICES = [
        ('Delhi', 'Delhi'),
        ('Bengaluru', 'Bengaluru'),
        ('Mumbai', 'Mumbai'),
        ('West Bengal', 'West Bengal'),
        ('Hyderabad', 'Hyderabad'),
        ('Chennai', 'Chennai'),
        ('Kolkata', 'Kolkata'),
        ('All India', 'All India'),
        ('Kerala', 'Kerala'),  # Added to match seed data
        ('Rural India', 'Rural India'),  # Added to match seed data
    ]

    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="General")
    scheme_type = models.CharField(max_length=50, choices=SCHEME_TYPE_CHOICES, default="Central Government")
    description = models.TextField(blank=True, null=True)
    eligibility = models.CharField(max_length=100, choices=ELIGIBILITY_CHOICES, blank=True, null=True)  # Increased max_length
    benefits = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default="All India")
    date = models.DateField(blank=True, null=True)  # Single date field to match seed data

    def __str__(self):
        return self.name


# -------------------- DOCUMENT MODEL --------------------
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name


# -------------------- USER PROFILE --------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    middle_name = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=100, blank=True)

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
    nation = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True)  # comma-separated

    def __str__(self):
        return self.user.username
