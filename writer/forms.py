from account.models import CustomUser
from .models import Article
from django.forms import ModelForm


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium', ]


class UpdateUserForm(ModelForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']
        exclude = ['password1', 'password2']
