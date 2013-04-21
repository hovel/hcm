from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from userena import views as userena_views
from hcm_profile.forms import HcmEditProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='hcm_home'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$', userena_views.profile_edit, kwargs={'edit_profile_form': HcmEditProfileForm},
       name='userena_profile_edit'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),
    url(r'^news/', include('hcm_news.urls')),
    url(r'^blog/', include('hcm_blog.urls')),
    url(r'^messages/', include('postman.urls')),
    url(r'^ajax_lookup/', include('ajax_select.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)