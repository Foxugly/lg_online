from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from customuser.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'