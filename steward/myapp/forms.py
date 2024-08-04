from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile, Feedback, Organization, WorkAddress, WorkJournalEntry
import requests

User = get_user_model()

class WorkerLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class StewardLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class OrganizationLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class OrganizationSignUpForm(UserCreationForm):
    organization_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Organization Name'}))
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}))
    position = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Position'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'organization_name', 'full_name', 'phone_number', 'address', 'position']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        user.user_type = 3  # Set user type to Organization
        if commit:
            user.save()
        return user

class WorkerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set email as the username
        user.email = self.cleaned_data['email']
        user.user_type = 1  # Set user type to Worker
        if commit:
            user.save()
        return user

class StewardSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    telephone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Telephone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set email as the username
        user.email = self.cleaned_data['email']
        user.user_type = 2  # Set user type to Steward
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    organization_name = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = Profile
        fields = ['organization_name', 'address']

    def clean_address(self):
        address = self.cleaned_data.get('address')
        organization_name = self.cleaned_data.get('organization_name')

        # Validate the address using the Google Places API
        validated_address, latitude, longitude = self.validate_address(address)

        if not validated_address:
            raise forms.ValidationError("Invalid address.")

        # Get or create the organization
        organization, created = Organization.objects.get_or_create(name=organization_name)

        # Check if the address already exists
        work_address, created = WorkAddress.objects.get_or_create(
            address=validated_address,
            organization=organization,
            defaults={'latitude': latitude, 'longitude': longitude}
        )

        return work_address

    def validate_address(self, address):
        api_key = 'AIzaSyA_SxDKGSuYaTRIeGfu6d0D3wfq1pKF7as'
        response = requests.get(
            f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json',
            params={
                'input': address,
                'inputtype': 'textquery',
                'fields': 'formatted_address,geometry',
                'key': api_key
            }
        )
        response_data = response.json()

        if not response_data.get('candidates'):
            return None, None, None

        result = response_data['candidates'][0]
        validated_address = result['formatted_address']
        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']

        return validated_address, latitude, longitude

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'private', 'feedback_type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'content': 'Your Feedback',
            'private': 'Private',
            'feedback_type': 'Type of Feedback',
        }

class WorkJournalEntryForm(forms.ModelForm):
    class Meta:
        model = WorkJournalEntry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'title': 'Entry Title',
            'content': 'Content',
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, help_text='Required', label="Email")
