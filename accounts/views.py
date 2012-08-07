# -*- coding: utf-8 -*-
import urlparse

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .models import UserProfile
from .forms import UserProfileForm, RegistrationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    if 'register' in request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.register(request)
            return redirect(reverse('accounts.views.complete_profile'))
    else:
        form = RegistrationForm()

    if 'login' in request.POST:
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            redirect_to = request.REQUEST.get('next', '')
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            login(request, auth_form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)
    else:
        auth_form = AuthenticationForm(request)

    request.session.set_test_cookie()

    ctx = {'form': form, 'auth_form': auth_form}
    return render(request, 'accounts/register.html', ctx)


@login_required
def complete_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    form = UserProfileForm(request.POST or None, instance=user_profile)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'accounts/complete_profile.html', {'form': form})
