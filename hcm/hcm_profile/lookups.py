from django.db.models import Q
from hcm_profile.models import MainUserProfile
from ajax_select import LookupChannel


class UserLookup(LookupChannel):

    model = MainUserProfile

    def get_query(self, q, request):
        return MainUserProfile.objects.\
            filter(Q(user__username__icontains=q) | Q(user__email__istartswith=q)).\
            exclude(user__username='Anonymous').\
            select_related('user').\
            order_by('user__username')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.user.username

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return obj.user.username