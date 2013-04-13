from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model

# Create your models here.
from django.core.urlresolvers import reverse
from pybb.models import PybbProfile
from userena.models import UserenaBaseProfile


class MainUserProfile(UserenaBaseProfile, PybbProfile):
    user = AutoOneToOneField(get_user_model(), related_name='hcm_profile')

    def get_mugshot_url(self):
        return self.avatar_url

    def get_absolute_url(self):
        return reverse('userena_profile_detail', kwargs={'username': self.user.get_username() })