from django import forms
from . import models
from user.models import User


class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='Titre',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=2048, label='Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', "image"]


class ReviewForm(forms.ModelForm):
    CHOICES = [
        ('1', '- 1 '),
        ('2', '- 2 '),
        ('3', '- 3 '),
        ('4', '- 4 '),
        ('5', '- 5 '),
    ]

    headline = forms.CharField(max_length=128, label='Titre',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    rating = forms.ChoiceField(choices=CHOICES, label='Note',
                               widget=forms.RadioSelect(attrs={'class': 'd-inline-flex gap-3'}))
    body = forms.CharField(max_length=8192, label='Commentaire',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]


class UserFollowsForm(forms.ModelForm):
    followed_user = forms.CharField(
        label="",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
    )

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_followed_user(self):
        username = self.cleaned_data['followed_user']

        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        if self.user == followed_user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        return followed_user
