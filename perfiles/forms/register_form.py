from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña", required=True)

    class Meta: 
        model = User
        fields = ["username", "password", "confirm_password"]

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")
            if password and confirm_password and password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            return cleaned_data