from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # make email field unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check if user with form.email exists
        user_count = User.objects.filter(email=email).count()
        # if len(email) <= 0:
            # raise forms.ValidationError("Email field is required")
        if user_count > 0:
            raise forms.ValidationError("A user with that email address already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check if user with form.email exists
        user_count = User.objects.filter(email=email).count()
        # if len(email) <= 0:
            # raise forms.ValidationError("Email field is required")
        if user_count > 0:
            raise forms.ValidationError("A user with that email address already exists.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']