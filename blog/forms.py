from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordResetForm,
    SetPasswordForm, PasswordChangeForm, UsernameField
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from blog.models import Post

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' , 'phone' , 'gender' , 'birthday' , 'username' ]
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        username = cleaned_data.get('username')
        birthday = cleaned_data.get('birthday')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if username and len(username) < 5:
            self.add_error('username', 'Minimum 5 characters required')

        if phone and len(phone) < 13:
            self.add_error('phone', 'Phone Should Contain a minimum of 13 characters')

        return cleaned_data


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', "picture"]

    def clean_title(self):
        title = self.cleaned_data['title']
        max_length = 100
        if len(title) > max_length:
            raise forms.ValidationError(
                f'Title length must not exceed {max_length} characters.'
            )
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        max_length = 2500
        if len(content) > max_length:
            raise forms.ValidationError(
                f'Content length must not exceed {max_length} characters.'
            )
        return content


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password Confirmation'}),
    )
    photo = forms.ImageField(label=_("Photo"),
                             required=False
                             )

    class Meta:
        model = User
        fields = ('username', 'email', 'photo')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email'
            })
        }


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Username"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password"}),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Old Password'
    }), label="New Password")
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
