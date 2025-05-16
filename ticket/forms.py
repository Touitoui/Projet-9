from django import forms

from . import models

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