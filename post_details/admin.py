from django.contrib import admin

from post_details.models import Post, Category, Like, Comment,Teacher

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Teacher)
