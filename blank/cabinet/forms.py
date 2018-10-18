from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm
from .models import Comment

class FormDownload(forms.Form):
    '''Скачать бланк'''
    title = forms.CharField(widget=forms.HiddenInput())
    blank = forms.CharField(widget=forms.HiddenInput())
    

#
class SignupForm(forms.ModelForm):
    '''Регистрация Пользователя '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {}
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True, 'autofocus':'autofocus'}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }

    def signup(self, request, user):
        user.save()

class LoginForm(LoginForm):
    '''Вход в личный кабинет'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Логин или e-mail"
        self.fields['login'].widget.attrs['placeholder'] = 'Логин или e-mail'

class UpdateProfileForm(forms.ModelForm):
    '''Обновление анкеты в личном кабинете'''
    class Meta:
        fields = ['first_name', 'last_name']
        model = User
    
class CommentForm(forms.ModelForm):
    ''' Комментарии в бланках '''
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Ваш комментарий'}
    
    