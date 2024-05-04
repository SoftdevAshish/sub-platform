from django.forms import ModelForm

from account.models import CustomUser


class UpdateUserForm(ModelForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
        exclude = ["email", "password1", "password2"]
