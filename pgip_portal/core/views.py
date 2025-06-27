from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import Truncator
from django.contrib import admin
from datetime import datetime
from .models import UserProfile, Scheme, Exam, TaxUpdate
from core.forms import UserProfileForm

# Admin registrations
admin.site.register(UserProfile)

# =======================
# Authentication Views
# =======================

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
                return redirect('dashboard')
            except UserProfile.DoesNotExist:
                return redirect('user_details')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already exists"})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'register.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        messages.success(request, f"Reset link sent to {email}")
    return render(request, 'forgot.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# =======================
# User Profile Views
# =======================

@login_required
def user_profile(request):
    return render(request, 'profile.html')

@login_required
def user_details_view(request):
    return render(request, 'user-details.html')

@login_required
def save_user_details(request):
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)

        profile.gender = request.POST.get('gender', '')
        profile.dob = request.POST.get('dob', '')  # this was missing!
        profile.interests = ",".join(request.POST.getlist('interests'))
        profile.qualification = request.POST.get('qualification', '')
        profile.income = request.POST.get('income', '')
        profile.employment_type = request.POST.get('employment_type', '')
        profile.caste_category = request.POST.get('caste_category', '')
        profile.location = request.POST.get('location', '')

        profile.save()
        return redirect('dashboard')

    return redirect('user_details')
from .models import UserExtendedProfile
from datetime import datetime
@login_required
def user_extended_profile_view(request):
    if request.method == 'POST':
        try:
            profile = UserExtendedProfile.objects.get(user=request.user)
        except UserExtendedProfile.DoesNotExist:
            profile = UserExtendedProfile(user=request.user)

        # ✅ Safe DOB parsing
        dob_str = request.POST.get('dob', '')
        try:
            profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        except (ValueError, TypeError):
            profile.dob = None

        profile.first_name = request.POST.get('first_name', '')  
        profile.middle_name = request.POST.get('middle_name', '')  
        profile.last_name = request.POST.get('last_name', '')  
        profile.father_name = request.POST.get('father_name', '')  
        profile.mother_name = request.POST.get('mother_name', '')  
        profile.marital_status = request.POST.get('marital_status', '')  
        profile.urban_rural = request.POST.get('urban_rural', '')  
        profile.religion = request.POST.get('religion', '')  
        profile.category = request.POST.get('category', '')  
        profile.disability = request.POST.get('disability', '')  
        profile.ex_serviceman = request.POST.get('ex_serviceman', '')  
        profile.priority_ex_service = request.POST.get('priority_ex_service', '')  
        profile.eyesight = request.POST.get('eyesight', '')  
        profile.chest = request.POST.get('chest') or 0  
        profile.height = request.POST.get('height') or 0  
        profile.weight = request.POST.get('weight') or 0  
        profile.address = request.POST.get('address', '')  
        profile.pin = request.POST.get('pin', '')  
        profile.locality = request.POST.get('locality', '')  
        profile.mobile = request.POST.get('mobile', '')  
        profile.email = request.POST.get('email', '')  
        profile.tel = request.POST.get('tel', '')  

        profile.save()
        return redirect('dashboard')

    return render(request, 'profile.html')


# =======================
# Dashboard & Features
# =======================

@login_required
def dashboard_view(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('user_details')

    interests = [i.strip().lower() for i in profile.interests.split(',') if i.strip()]
    recommendations = []

    # Static Recommendations
    static_recs = {
        'jobs': "🧑‍💼 Jobs available matching your education and employment type.",
        'sports': "🎽 Sports schemes and tournaments in your region.",
        'news': "📰 Latest government news, reforms, and policy updates.",
        'feedback': "📢 Submit your feedback to improve governance.",
        'environment': "🌱 Environmental programs and green initiatives.",
        'technology': "💻 Tech innovation challenges and IT schemes.",
        'health': "🏥 Health insurance and wellness programs.",
        'women empowerment': "👩‍🧠 Schemes for women empowerment and safety.",
        'social welfare': "🦳 Social welfare schemes for senior citizens, differently-abled, etc."
    }

    for key, message in static_recs.items():
        if key in interests:
            recommendations.append(message)

    if not recommendations:
        recommendations.append("ℹ No recommendations found yet. Please update your interests or try again later.")

    return render(request, 'dashboard.html', {'recs': recommendations})

# =======================
# Dashboard Pages
# =======================

@login_required
def find_schemes_view(request):
    return render(request, 'find-schemes.html')

@login_required
def upload_docs_view(request):
    return render(request, 'upload-docs.html')

@login_required
def track_applications_view(request):
    return render(request, 'track-applications.html')

@login_required
def help_center_view(request):
    return render(request, 'help-center.html')

@login_required
def apply_scheme_view(request, scheme_name):
    return render(request, 'apply-scheme.html', {'scheme_name': scheme_name})