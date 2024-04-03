from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm, UsernameField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from blog.models import Post

User = get_user_model()


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, label=_('First Name'))
    last_name = forms.CharField(max_length=255, label=_('Last Name'))
    email = forms.EmailField(label=_('Email'))
    phone = forms.CharField(max_length=15, label=_('Phone'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+380'):
            raise ValidationError(_('Phone number must start with +380'))
        if len(phone) != 13:
            raise ValidationError(_('Phone number must be 13 characters long'))
        return phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        if phone:
            try:
                self.clean_phone()
            except ValidationError as e:
                self.add_error('phone', e)
        return cleaned_data


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', "picture"]

    def clean_title(self):
        title = self.cleaned_data['title']
        max_length = 30
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
