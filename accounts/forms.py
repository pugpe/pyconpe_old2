# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class RegistrationForm(forms.Form):
    '''
    Baseado em https://bitbucket.org/ubernostrum/django-registration/
    '''
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$', max_length=30,
        widget=forms.TextInput(), label=_(u'Username'),
        error_messages={
            'invalid': _(u'This value may contain only letters, numbers and '
                         u'@/./+/-/_ characters.')
        },
    )

    email = forms.EmailField(max_length=75, label=_(u'E-mail'))

    password1 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_("Password"),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_("Password (again)"),
    )

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'],
        )
        if existing.exists():
            raise forms.ValidationError(
                _(u'Já existe um usuário cadastrado com esse nome de '
                  u'usuário'),
            )
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        cleaned_data = self.cleaned_data
        if 'password1' in cleaned_data and 'password2' in cleaned_data:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError(
                    _(u'Os campos de senha não batem'),
                )
        return cleaned_data

    def register(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']

        User.objects.create_user(username, email, password)

        user = authenticate(username=username, password=password)
        login(request, user)

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
