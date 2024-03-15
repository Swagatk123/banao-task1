from django.contrib import admin
from .models import User , BlogPost,Category,Appointment
# Register your models here.
admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Appointment)