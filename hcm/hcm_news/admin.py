from django.contrib import admin
from hcm_news.models import News


class NewsAdmin(admin.ModelAdmin):
    exclude = ('author', )
    prepopulated_fields = {'slug': ('title', )}
    date_hierarchy = 'date_published'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super(NewsAdmin, self).save_model(request, obj, form, change)


admin.site.register(News, NewsAdmin)