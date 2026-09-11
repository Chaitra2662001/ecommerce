from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )