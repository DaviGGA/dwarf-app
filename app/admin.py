from django.contrib import admin

from app.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)