from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/events/', views.api_events, name='api_events'),
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    path('login/', views.login_request, name='login'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    path('delete-reminder/<int:task_id>/', views.delete_reminder, name='delete_reminder'),
    path('documents/', views.documents, name='documents'),
    path('delete-document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('search/', views.search_results, name='search_results'),
    path('register/<str:item_type>/<str:item_name>/', views.demo_register, name='demo_register'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('scheme/<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),
    path('exam/<int:item_id>/register/', views.demo_register, {'item_type': 'exam'}, name='exam_detail'),
    path('scheme/<int:item_id>/register/', views.demo_register, {'item_type': 'scheme'}, name='scheme_detail'),
    path('success/', views.registration_success, name='registration_success'),
]
