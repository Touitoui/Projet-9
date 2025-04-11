from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from . import models
from . import forms
from review import models as review_model
from itertools import chain



def home(request):
    if request.user.is_authenticated:
        reviews = review_model.Review.objects.all()
        tickets = models.Ticket.objects.all()

        # Combine reviews and tickets into one list
        # and sort by date (newest first)
        ticketsreviews = sorted(
            chain(reviews, tickets),
            key=lambda item: item.time_created,  # Adjust this field name based on your model
            reverse=True
        )
        return render(request, 'flux.html', context={'ticketsreviews': ticketsreviews})
    else:
        return redirect('login')  

@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('/')
    return render(request, 'forms/create_ticket.html', context={'form': form})

@login_required
def ticket_update(request, id):
    try:
        ticket = models.Ticket.objects.get(id=id)
    except models.Ticket.DoesNotExist:
        return HttpResponse("Ticket non trouvé.", status=404)
    
    if request.user != ticket.user:
        return HttpResponse("Vous n'avez pas la permission de modifier ce ticket.", status=403)
    
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('/')
    else:
        form = forms.TicketForm(instance=ticket)
    return render(request, 'forms/update_ticket.html', context={'form': form})

@login_required
def ticket_delete(request, id):
    try:
        ticket = models.Ticket.objects.get(id=id)
    except models.Ticket.DoesNotExist:
        return HttpResponse("Ticket non trouvé.", status=404)
    
    if request.user != ticket.user:
        return HttpResponse("Vous n'avez pas la permission de supprimer ce ticket.", status=403)
    
    if request.method == 'POST':
        ticket.delete()
        return redirect('/')
    return render(request, 'forms/delete_ticket.html', context={'form': ticket})