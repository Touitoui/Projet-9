from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from . import models
from . import forms


@login_required
def follow_user(request):
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
def unfollow_user(request, id):
    try:
        user_follow = models.UserFollows.objects.get(id=id)
    except models.UserFollows.DoesNotExist:
        return HttpResponse("Abonnement non trouvé.", status=404)
    
    if request.user != user_follow.user:
        return HttpResponse("Vous n'avez pas la permission.", status=403)
    
    if request.method == 'POST':
        user_follow.delete()
        return redirect('follow_user')
    return render(request, 'forms/unfollow_user.html', context={'user_follow': user_follow})