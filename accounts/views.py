# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import UserProfile
from .forms import UserProfileForm, RegistrationForm


def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.register(request)
        return redirect(reverse('accounts.views.complete_profile'))

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def complete_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    form = UserProfileForm(request.POST or None, instance=user_profile)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'accounts/complete_profile.html', {'form': form})
