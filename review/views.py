from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from . import models
from . import forms
from ticket import forms as ticket_forms

@login_required
def review_upload(request):
    form_ticket = ticket_forms.TicketForm()
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_ticket = ticket_forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST)
        if all([form_review.is_valid(), form_ticket.is_valid()]):
            print("post ticket")

            ticket = form_ticket.save(commit=False)
            ticket.user = request.user            
            ticket.save()
            print("-------")
            print(ticket)
            
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket

            review.save()
            return redirect('/')
        
    context = {
        'form_review': form_review,
        'form_ticket': form_ticket,
    }
    return render(request, 'forms/create_review.html', context=context)


@login_required
def review_update(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return HttpResponse("Critique non trouvé.", status=404)
    
    if request.user != review.user:
        return HttpResponse("Vous n'avez pas la permission de modifier cette critique.", status=403)
    
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('/')
    else:
        form = forms.ReviewForm(instance=review)
    return render(request, 'forms/update_review.html', context={'form': form})

@login_required
def review_delete(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return HttpResponse("Critique non trouvé.", status=404)
    
    if request.user != review.user:
        return HttpResponse("Vous n'avez pas la permission de supprimer cette critique.", status=403)
    
    if request.method == 'POST':
        review.delete()
        return redirect('/')
    return render(request, 'forms/delete_review.html', context={'form': review})