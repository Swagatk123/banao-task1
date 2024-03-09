from django.contrib import admin
from .models import User , BlogPost,Category
# Register your models here.
admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Category)