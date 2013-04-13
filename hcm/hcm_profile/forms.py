from userena.forms import EditProfileForm


class HcmEditProfileForm(EditProfileForm):
    class Meta(EditProfileForm.Meta):
        fields = ['signature', 'time_zone', 'language', 'show_signatures', 'avatar', 'privacy']