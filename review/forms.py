from django import forms

from . import models

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