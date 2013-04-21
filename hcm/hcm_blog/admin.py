from django.contrib import admin
from hcm_blog.models import Post


class BlogPostAdmin(admin.ModelAdmin):
    exclude = ('author', 'body_html', )
    prepopulated_fields = {'slug': ('title', )}
    date_hierarchy = 'date_published'
    list_display = ('title', 'author', 'date_published', 'is_published', )
    list_editable = ('is_published', )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super(BlogPostAdmin, self).save_model(request, obj, form, change)


admin.site.register(Post, BlogPostAdmin)