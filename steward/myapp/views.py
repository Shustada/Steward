from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    OrganizationSignUpForm, WorkerSignUpForm, ProfileForm, FeedbackForm, StewardSignUpForm, CustomLoginForm
)
from .models import Profile, Feedback, CommunityEntry, Organization, WorkAddress, CustomUser

def home(request):
    open_tab = request.GET.get('open_tab', 'Worker')
    worker_login_form = CustomLoginForm()
    steward_login_form = CustomLoginForm()
    organization_login_form = CustomLoginForm()
    return render(request, 'home.html', {
        'open_tab': open_tab,
        'worker_login_form': worker_login_form,
        'steward_login_form': steward_login_form,
        'organization_login_form': organization_login_form
    })

def organization_signup(request):
    if request.method == 'POST':
        form = OrganizationSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('organization_dashboard')
    else:
        form = OrganizationSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Organization'})

def organization_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None and user.user_type == 3:  # Ensure user is of type Organization
                login(request, user)
                return redirect('organization_dashboard')
            else:
                messages.error(request, 'Invalid email, password, or user type.')
    else:
        form = CustomLoginForm()
    return render(request, 'home.html', {'organization_login_form': form, 'open_tab': 'Organization'})

def steward_signup(request):
    if request.method == 'POST':
        form = StewardSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect(f"{reverse('home')}?open_tab=Steward")
    else:
        form = StewardSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Steward'})

def steward_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None and user.user_type == 2:  # Ensure user is of type Steward
                login(request, user)
                return redirect('steward_dashboard')
            else:
                messages.error(request, 'Invalid email, password, or user type.')
    else:
        form = CustomLoginForm()
    return render(request, 'home.html', {'steward_login_form': form, 'open_tab': 'Steward'})

def worker_signup(request):
    if request.method == 'POST':
        form = WorkerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Successfully registered. Please log in.')
            return redirect(f"{reverse('home')}?open_tab=Worker")
    else:
        form = WorkerSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Worker'})

def worker_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None and user.user_type == 1:  # Ensure user is of type Worker
                login(request, user)
                return redirect('worker_dashboard')
            else:
                messages.error(request, 'Invalid email, password, or user type.')
    else:
        form = CustomLoginForm()
    return render(request, 'home.html', {'worker_login_form': form, 'open_tab': 'Worker'})

@login_required
def complete_profile(request):
    if hasattr(request.user, 'profile'):
        profile_instance = request.user.profile
    else:
        profile_instance = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.work_address = form.cleaned_data['address']
            organization_name = form.cleaned_data['organization_name']
            organization, created = Organization.objects.get_or_create(name=organization_name)
            profile.organization = organization
            profile.is_profile_complete = True  # Mark profile as complete
            profile.save()
            return redirect('worker_dashboard')
        else:
            print(form.errors)  # Debug: Print form errors if the form is invalid
    else:
        form = ProfileForm(instance=profile_instance)

    return render(request, 'complete_profile.html', {'form': form})

@login_required
def worker_dashboard(request):
    work_address = request.user.profile.work_address
    feedback_entries = Feedback.objects.filter(user=request.user)  # Assuming you want to show user-specific feedback

    context = {
        'work_address': work_address,
        'feedback_entries': feedback_entries,
    }

    return render(request, 'worker_dashboard.html', context)

@login_required
def contact_steward(request):
    work_address = request.user.profile.work_address
    
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_entry = feedback_form.save(commit=False)
            feedback_entry.work_address = work_address
            if request.POST.get('anonymous'):
                feedback_entry.user = None
            else:
                feedback_entry.user = request.user
            feedback_entry.save()
            return redirect('contact_steward')
    else:
        feedback_form = FeedbackForm()

    feedback_entries = Feedback.objects.filter(work_address=work_address)
    context = {
        'work_address': work_address,
        'feedback_form': feedback_form,
        'feedback_entries': feedback_entries,
    }
    return render(request, 'contact_steward.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html') 

@login_required
def roster(request):
    return render(request, 'roster.html') 

@login_required
def resources(request):
    return render(request, 'resources.html')  # Ensure you have a resources.html template

@login_required
def work_journal(request):
    return render(request, 'work_journal.html')  # Ensure you have a work_journal.html template

@login_required
def steward_dashboard(request):
    # Placeholder view for steward dashboard
    return render(request, 'steward_dashboard.html')

@login_required
def organization_dashboard(request):
    # Placeholder view for organization dashboard
    return render(request, 'organization_dashboard.html')

@login_required
def manage_workers(request):
    return render(request, 'manage_workers.html')

@login_required
def generate_reports(request):
    return render(request, 'generate_reports.html')

@login_required
def post_announcements(request):
    return render(request, 'post_announcements.html')

@login_required
def steward_settings(request):
    return render(request, 'steward_settings.html')

@login_required
def view_worker_submissions(request):
    # Get the work address for the logged-in steward
    steward_profile = request.user.profile
    steward_work_address = steward_profile.work_address

    print(f"Steward Work Address: {steward_work_address}")
    
    # Fetch feedback submissions for the steward's work address
    feedback_entries = Feedback.objects.filter(work_address=steward_work_address)
    
    print(f"Feedback Entries: {feedback_entries}")
    
    context = {
        'feedback_entries': feedback_entries,
        'work_address': steward_work_address
    }
    
    return render(request, 'worker_submissions.html', context)