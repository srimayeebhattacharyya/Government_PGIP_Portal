"""
URL configuration for pgip_portal project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views 
from core.views import user_events_api 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('profile/', views.user_profile, name='user_profile'),
    path('save-details/', views.save_user_details, name='save_details'),
    path('my-profile/', views.user_extended_profile_view, name='user_profile_view'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('user_details/', views.user_details_view, name='user_details'),

    # Dashboard sections
    path('find-schemes/', views.find_schemes_view, name='find_schemes'),
    path('upload-documents/', views.upload_docs_view, name='upload_docs'),
    path('track-applications/', views.track_applications_view, name='track_applications'),
    path('help-center/', views.help_center_view, name='help_center'),
    path('apply/<str:scheme_name>/', views.apply_scheme_view, name='apply_scheme'),

    # ✅ APIs
    path('api/exams/', views.exams_json, name='exams_json'),  # should return exams as JSON
    path('api/user-events/', user_events_api, name='user_events_api'),  # your new calendar events API
]