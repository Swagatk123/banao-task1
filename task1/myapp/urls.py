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
    path('error/',Error,name="error"),
    path('createblog/',create_blog,name='create_blog'),
    path('yourblogs/',doctorsBlog,name='doctorsblog'),
    path('readblog/<int:id>/',read_more,name='read_more'),
    path('editblog/<int:id>/',edit_blog,name='edit_blog'),
    path('allblog/',allBlog,name='allblog'),
    path('mentalhealth/',mental,name='mental_health'),
    path('heartdisease/',Heart,name='Heart_Disease'),
    path('covid/',Covid,name='Covid'),
    path('immunization/',Immune,name='Immunization'),
    path('unauthorized/',unauthorized,name='unauthorized'),
    path('doctorslist/',list_doctors,name='doctorslist'),
    path('bookappointment/<int:doctor_id>/',book_appointment,name='bookappointment'),
    path('appointmentconfirmation<int:appointment_id>/',appointment_confirmation,name='appointment_confirmation')
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)