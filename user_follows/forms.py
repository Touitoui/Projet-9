from django import forms

from . import models
from user.models import User

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
            # followed_user = User.objects.get(username__iexact=username) #  Allow case-insensitive matching ?
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        
        if self.user == followed_user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")
            
        return followed_user