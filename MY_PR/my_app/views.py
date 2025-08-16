from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from calendar import monthrange
import random
import json
from .forms import UserForm, UserProfileForm
from .forms import UserProfileForm
from .models import UserProfile
from .models import OTP, Task, Exam, Scheme, Document
from .forms import EmailForm, OTPForm, TaskForm, DocumentForm

# Dummy data for jobs and schemes
DUMMY_SCHEMES = [f"Scheme {i}" for i in range(1, 31)]
DUMMY_JOBS = [f"Job {i}" for i in range(1, 31)]

# Dashboard
def dashboard(request):
    query = request.GET.get('q', '').lower()
    exams = Exam.objects.all()
    schemes = Scheme.objects.all()

    if query:
        exams = exams.filter(name__icontains=query)
        schemes = schemes.filter(name__icontains=query)

    return render(request, 'dashboard.html', {
        'exams': exams,
        'schemes': schemes,
        'query': request.GET.get('q', '')
    })

# Search Feature
def search_results(request):
    query = request.GET.get('q')
    exams = []
    schemes = []

    if query:
        exams = Exam.objects.filter(name__icontains=query)
        schemes = Scheme.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'exams': exams,
        'schemes': schemes
    }

    return render(request, 'search_results.html', context)

def demo_register(request, item_type, item_id):
    if request.method == "POST":
        return render(request, 'success.html', {'item_type': item_type})
    return render(request, 'demo_register.html', {'item_type': item_type})

def registration_success(request):
    return render(request, 'success.html')



def contact_view(request):
    return render(request, 'contact.html')

# Calendar Page
def calendar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    today = datetime.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    month_days = monthrange(year, month)[1]

    tasks = Task.objects.filter(user=request.user, date__year=year, date__month=month)
    calendar_days = []

    for day in range(1, month_days + 1):
        current_date = datetime(year, month, day)
        is_sunday = current_date.weekday() == 6
        day_tasks = tasks.filter(date=current_date.date())
        calendar_days.append({
            'day': day,
            'date': current_date.date(),
            'tasks': day_tasks,
            'is_sunday': is_sunday,
        })

    if request.method == 'POST':
        if 'add' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('calendar')
        elif 'delete' in request.POST:
            Task.objects.filter(id=request.POST.get('task_id')).delete()
            return redirect('calendar')
    else:
        form = TaskForm()

    context = {
        'calendar_days': calendar_days,
        'form': form,
        'year': year,
        'month': month,
    }
    return render(request, 'calendar.html', context)

# Login and OTP
def send_otp_email(user):
    otp = f"{random.randint(100000, 999999)}"
    OTP.objects.update_or_create(user=user, defaults={"otp_code": otp, "created_at": timezone.now()})
    send_mail(
        subject='Your OTP Code',
        message=f'Hi {user.username},\n\nYour OTP for login is: {otp}\n\nThis will expire in 10 minutes.',
        from_email='youremail@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )

def login_request(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user, _ = User.objects.get_or_create(username=email, email=email)
            send_otp_email(user)
            request.session['user_id'] = user.id
            return redirect('verify_otp')
    else:
        form = EmailForm()
    return render(request, 'login.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            try:
                otp_obj = OTP.objects.get(user=user)
                if otp_obj.otp_code == otp_input:
                    if otp_obj.is_expired():
                        form.add_error(None, "OTP has expired. Please login again.")
                    else:
                        login(request, user)
                        return redirect('dashboard')
                else:
                    form.add_error('otp', "Invalid OTP.")
            except OTP.DoesNotExist:
                form.add_error(None, "OTP not found. Please login again.")
    else:
        form = OTPForm()
    return render(request, 'otp.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# API for FullCalendar
def api_events(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    tasks = Task.objects.filter(user=request.user)
    events = [{"id": t.id, "title": t.title, "start": str(t.date)} for t in tasks]
    return JsonResponse(events, safe=False)

@csrf_exempt
def add_reminder(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            title = data.get('title')
            date = data.get('date')
            if title and date:
                Task.objects.create(user=request.user, title=title, date=date)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Missing title or date"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

@csrf_exempt
def delete_reminder(request, task_id):
    if request.method == "DELETE" and request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({"status": "success"})
        except Task.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Task not found"})
    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

# Document Uploads
@login_required
def documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect('documents')
    else:
        form = DocumentForm()

    docs = Document.objects.filter(user=request.user)
    return render(request, 'documents.html', {'form': form, 'documents': docs})

@login_required
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, user=request.user)
    if request.method == 'POST':
        doc.file.delete()
        doc.delete()
    return redirect('documents')

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        return render(request, 'success.html', {'item_name': exam.name})
    return render(request, 'exam_detail.html', {'exam': exam})

def scheme_detail(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    if request.method == 'POST':
        return render(request, 'success.html', {'item_name': scheme.name})
    return render(request, 'scheme_detail.html', {'scheme': scheme})




def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Document  # if you have a Document model

@login_required(login_url='login')
def documents_view(request):
    documents = Document.objects.filter(user=request.user)  # example
    return render(request, 'documents.html', {'documents': documents})

