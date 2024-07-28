from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('organization/signup/', views.organization_signup, name='organization_signup'),
    path('organization/login/', views.organization_login, name='organization_login'),
    path('steward/signup/', views.steward_signup, name='steward_signup'),
    path('steward/login/', views.steward_login, name='steward_login'),
    path('worker/signup/', views.worker_signup, name='worker_signup'),
    path('worker/login/', views.worker_login, name='worker_login'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('contact-steward/', views.contact_steward, name='contact_steward'),
    path('profile/', views.profile, name='profile'),
    path('roster/', views.roster, name='roster'),
    path('resources/', views.resources, name='resources'),
    path('work-journal/', views.work_journal, name='work_journal'),
    path('steward/dashboard/', views.steward_dashboard, name='steward_dashboard'),
    path('organization/dashboard/', views.organization_dashboard, name='organization_dashboard'),
    path('manage-workers/', views.manage_workers, name='manage_workers'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('post-announcements/', views.post_announcements, name='post_announcements'),
    path('steward/settings/', views.steward_settings, name='steward_settings'),
    path('view-worker-submissions/', views.view_worker_submissions, name='view_worker_submissions'),
]
