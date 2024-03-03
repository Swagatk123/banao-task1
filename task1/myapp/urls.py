from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',Index),
    path('register/',register,name='register'),
    path('login',login_view,name='login_view'),
    path('patient',Patient,name='Patient'),
    path('doctor',Doctor,name='Doctor'),
    path('',Home,name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('error/',Error,name="error")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)