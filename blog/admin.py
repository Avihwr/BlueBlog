from django.contrib import admin
from blog.models import Blog, Contact, BlogComment, Profile, Excerpt


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'slug', 'time')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'time')


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'parent', 'time')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


class ExcerptAdmin(admin.ModelAdmin):
    list_display = ('excerpt',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Excerpt, ExcerptAdmin)
