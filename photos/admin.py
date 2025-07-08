from django.contrib import admin
from photos.models import Photo, Like, Comment


class PhotoAdmin(admin.ModelAdmin):
    fields = ['photo','description','location','tagged_pet','owner']

class LikeAdmin(admin.ModelAdmin):
    fields = ['user', 'photo']

class CommentAdmin(admin.ModelAdmin):
    fields = ['content']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)