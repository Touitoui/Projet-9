from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})

    username = forms.CharField(max_length=63, label='')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='')


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer mot de passe'})
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', )

    username = forms.CharField(max_length=63, label='')
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput, label='')
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput, label='')
