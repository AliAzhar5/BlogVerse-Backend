from django.contrib import admin
from v1.post.models import Post, Likes,Profile

admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Profile)
