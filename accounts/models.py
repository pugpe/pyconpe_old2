# -*- coding: utf-8 -*-
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


OPT = {'null': True, 'blank': True}

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    name = models.CharField(_(u'Nome'), max_length=100, **OPT)
    about = models.TextField(_(u'Sobre'))
    site = models.URLField(_(u'Site'), **OPT)
    occupation = models.CharField(_(u'Ocupação'), max_length=100, **OPT)
    institution = models.CharField(
        _(u'Universidade / Empresa / Grupo'), max_length=100, **OPT
    )

    public = models.BooleanField(_(u'Perfil público?'), default=True)

    def gravatar_url(self, size=110):
        hash = hashlib.md5(self.user.email).hexdigest()
        return 'http://gravatar.com/avatar/{0}?s={1}'.format(hash, size)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
