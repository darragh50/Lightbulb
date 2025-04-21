from django.contrib import admin
from .models import *
# Register your models here.
# Regiestering all models from models.py to the django admin site

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Followers)