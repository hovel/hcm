from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model

# Create your models here.
from pybb.models import PybbProfile
from userena.models import UserenaBaseProfile


class MainUserProfile(UserenaBaseProfile, PybbProfile):
    user = AutoOneToOneField(get_user_model(), related_name='hcm_profile')