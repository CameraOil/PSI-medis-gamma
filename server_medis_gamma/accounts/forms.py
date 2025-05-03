from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm,ReadOnlyPasswordHashField
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        # Include 'email' as it's your USERNAME_FIELD
        # 'password' and 'password2' are added automatically by UserCreationForm
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users in the admin.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default 'username' field if it's not part of your model
        if 'username' in self.fields:
             del self.fields['username']

    class Meta:
        model = User
        # List all the fields you want to be editable in the admin change form
        fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        # Note: 'password' field is handled separately by UserChangeForm via a "change password" link

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))
