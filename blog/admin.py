from django.contrib import admin

from blog.models import User, Post, Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
# Register your models here.
