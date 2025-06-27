from django.contrib.auth.models import User
from django.db import models # type: ignore

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    interests = models.CharField(max_length=255)
    qualification = models.CharField(max_length=50)
    income = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50, blank=True)
    caste_category = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return self.user.username
    
class UserExtendedProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    urban_rural = models.CharField(max_length=10, blank=True)
    religion = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=20, blank=True)
    disability = models.CharField(max_length=10, blank=True)
    ex_serviceman = models.CharField(max_length=10, blank=True)
    priority_ex_service = models.CharField(max_length=10, blank=True)
    eyesight = models.CharField(max_length=20, blank=True)
    chest = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    address = models.TextField(blank=True)
    pin = models.CharField(max_length=10, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - Extended Profile"

class Scheme(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    target_gender = models.CharField(max_length=20, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    income_range = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    qualification_required = models.CharField(max_length=100)
    applicable_states = models.CharField(max_length=200)
    date = models.DateField()
    def __str__(self):
        return self.title

class TaxUpdate(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    applicable_to_income_range = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class UserCalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on {self.date} by {self.user.username}"
