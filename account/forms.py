from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'is_writer']
