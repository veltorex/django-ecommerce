from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password Confirm",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean(self):
        cleaned_data = super().clean()

        # Get passwords
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password2"])

        if commit:
            user.save()

        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_staff"]
            
        