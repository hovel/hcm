from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from userena import views as userena_views
from hcm_profile.forms import HcmEditProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$', userena_views.profile_edit, kwargs={'edit_profile_form': HcmEditProfileForm},
       name='userena_profile_edit'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),
    url(r'^messages/', include('postman.urls')),
    url(r'^ajax_lookup', include('ajax_select.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)