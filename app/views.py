from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from itertools import chain
from django.db.models import Q
from . import models
from . import forms


def home(request):
    """
    Display the home page with a feed of tickets and reviews from the user and followed users.
    If user is authenticated, shows a chronological feed of their own tickets/reviews
    and those from users they follow.
    If not authenticated, redirects to login page.
    """
    if request.user.is_authenticated:
        followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

        reviews = models.Review.objects.filter(
            Q(user=request.user) | Q(user__in=followed_users)
        )
        tickets = models.Ticket.objects.filter(
            Q(user=request.user) | Q(user__in=followed_users)
        )

        ticketsreviews = sorted(
            chain(reviews, tickets),
            key=lambda item: item.time_created,
            reverse=True
        )
        return render(request, 'flux_page.html', context={'ticketsreviews': ticketsreviews})
    else:
        return redirect('login')


@login_required
def my_posts(request):
    """Display all posts (tickets and reviews) created by the authenticated user."""
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    ticketsreviews = sorted(
        chain(reviews, tickets),
        key=lambda item: item.time_created,
        reverse=True
    )
    return render(request, 'posts_page.html', context={'ticketsreviews': ticketsreviews})


@login_required
def ticket_upload(request):
    """Handle ticket creation with file upload."""
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('/')
    return render(request, 'forms/create_ticket.html', context={'form': form})


@login_required
def ticket_update(request, id):
    """Handle ticket update with permission checks and form validation."""
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
    """Delete a ticket if the user has permission. First call the confirmation page, then delete if user confirmed."""
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


@login_required
def new_review_upload(request):
    """Handle creation of a new review with an associated ticket."""
    form_ticket = forms.TicketForm()
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_ticket = forms.TicketForm(request.POST, request.FILES)
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
    return render(request, 'forms/new_review.html', context=context)


@login_required
def add_review(request, id_):
    """Creates a review for an existing ticket."""
    ticket = models.Ticket.objects.get(id=id_)
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        if all([form_review.is_valid()]):
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket

            review.save()
            return redirect('/')

    context = {
        'ticket': ticket,
        'form_review': form_review,
    }
    return render(request, 'forms/add_review.html', context=context)


@login_required
def review_update(request, id_):
    """Updates an existing review."""
    try:
        review = models.Review.objects.get(id=id_)
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
def review_delete(request, id_):
    """Delete a review if the user has permission. First call the confirmation page, then delete if user confirmed."""
    try:
        review = models.Review.objects.get(id=id_)
    except models.Review.DoesNotExist:
        return HttpResponse("Critique non trouvé.", status=404)

    if request.user != review.user:
        return HttpResponse("Vous n'avez pas la permission de supprimer cette critique.", status=403)

    if request.method == 'POST':
        review.delete()
        return redirect('/')
    return render(request, 'forms/delete_review.html', context={'form': review})


@login_required
def follow_user(request):
    """Handle user following functionality with form processing and display followed users and followers."""
    form = forms.UserFollowsForm()
    if request.method == 'POST':
        form = forms.UserFollowsForm(request.POST or None, user=request.user)
        if form.is_valid():
            user_follows = form.save(commit=False)
            user_follows.user = request.user
            user_follows.save()
            return redirect('follow_user')

    followed_users = models.UserFollows.objects.filter(user=request.user)
    followers = models.UserFollows.objects.filter(followed_user=request.user)

    context = {
        'form': form,
        'followed_users': followed_users,
        'followers': followers,
    }
    return render(request, 'followed_user_page.html', context=context)


@login_required
def unfollow_user(request, id_):
    """Unfollow a user by deleting the UserFollows relationship."""
    try:
        user_follow = models.UserFollows.objects.get(id=id_)
    except models.UserFollows.DoesNotExist:
        return HttpResponse("Abonnement non trouvé.", status=404)

    if request.user != user_follow.user:
        return HttpResponse("Vous n'avez pas la permission.", status=403)

    if request.method == 'POST':
        user_follow.delete()
        return redirect('follow_user')
    return render(request, 'forms/unfollow_user.html', context={'user_follow': user_follow})
