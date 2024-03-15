from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm,BlogPostForm,AppointmentForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BlogPost,User,Appointment
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
import json
import requests
# Create your views here.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
def Index(request):
    return render(request,'myapp/base.html')

def list_doctors(request):
    doctors = User.objects.filter(is_doctor=True)
    return render(request, 'myapp/alldoctors.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    doctor = User.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            speciality = form.cleaned_data['required_speciality']
            date = form.cleaned_data['date_of_appointment']
            start_time = form.cleaned_data['start_time_of_appointment']
            start_datetime = datetime.combine(date, start_time)
            end_datetime = start_datetime + timedelta(minutes=45)
            create_calendar_event(doctor.first_name,doctor.email, date, start_time)
            appointment = Appointment(doctor=doctor,required_speciality=speciality, date=date, start_time=start_time, end_time=end_datetime)
            appointment.save()

            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'myapp/book_appointment.html', {'doctor': doctor, 'form': form})

# def create_calendar_event(doctor_name, date, start_time):
#     creds = Credentials.from_authorized_user_file("myapp/creds.json", SCOPES)
#     service = build('calendar', 'v3', credentials=creds)
#     event = {
#         'summary': f'Appointment with {doctor_name}',
#         'description': 'Appointment booked through your application',
#         'start': {
#             'dateTime': f'{date}T{start_time}:00',
#             'timeZone': 'Asia/Kolkata',
#         },
#         'end': {
#             'dateTime': f'{date}T{start_time}:00',
#             'timeZone': 'Asia/Kolkata',
#         },
#     }
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print('Event created: %s' % (event.get('htmlLink')))

API_KEY = 'AIzaSyARsjMLfFTwl-QpAIytUROgLg_CSCrQsvk'
from google.oauth2 import service_account
import googleapiclient.discovery
SERVICE_ACCOUNT_FILE = 'myapp/noble-velocity-417305-fbb507a57fa4.json'
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

def create_calendar_event(doctor_name,doctor_email, date, start_time):

    event = {
        'summary': f'Appointment with {doctor_name}',
        'description': 'Appointment booked through your application',
        'start': {
            'dateTime': f'{date}T{start_time}:00',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': f'{date}T{start_time}:00',
            'timeZone': 'Asia/Kolkata',
        },
    }

    try:
        service.events().insert(calendarId=doctor_email, body=event).execute()
        print('Event created successfully.')
    except Exception as e:
        print('An error occurred:', e)

def appointment_confirmation(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'myapp/appointment_confirmation.html', {'appointment': appointment})


def register(request):
    msg = None
    if request.method == "POST":
        form  = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            msg = "User Created"
            return redirect('login_view')
        else:
            msg  = 'Form is not valid'
    else:
        form  = SignUpForm()
    return render(request,'myapp/register.html',{'form':form,'msg':msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_doctor:
                login(request,user)
                return redirect('Doctor')
            elif user is not None and user.is_patient:
                login(request,user)
                return redirect('Patient')
            else:
                msg = 'invalid'
        else:
            msg = 'error validating form'
    return render(request,'myapp/login.html',{'form':form,'msg':msg})


def create_blog(request):
    if not request.user.is_doctor:
        return redirect('unauthorized')
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']
            is_draft = form.cleaned_data['is_draft']
            author = request.user
            reg = BlogPost(title=title,image=image,category=category,summary=summary,content=content,is_draft=is_draft,author=author)
            reg.save()
            return redirect('Doctor')
    else:
        form = BlogPostForm()
    return render(request, 'myapp/createblog.html', {'form': form})

def doctorsBlog(request):
    if not request.user.is_doctor:
        return redirect('unauthorized')
    user = request.user
    blogs = BlogPost.objects.filter(author=user)
    
    return render(request,'myapp/doctorsblog.html',{'blog_posts':blogs})

def read_more(request,id):
    blog_details = BlogPost.objects.get(id=id)
    return render(request,'myapp/readblog.html',{'post':blog_details})

def unauthorized(request):
    return render(request,'myapp/unauthorized.html')

def edit_blog(request,id):
    if request.user.is_authenticated:
        if not request.user.is_doctor:
            return redirect('unauthorized')
        if request.method == "POST":
            blog_details = BlogPost.objects.get(id=id)
            form = BlogPostForm(request.POST,instance=blog_details)
            if form.is_valid():
                form.save()
                return redirect('doctorsblog')
        else:
            blog_details = BlogPost.objects.get(id=id)
            form = BlogPostForm(instance=blog_details)
        return render(request,"myapp/editblog.html",{'form':form})
    else:
        return redirect('dashboard')
    
def allBlog(request):
    allblogs = BlogPost.objects.filter(is_draft=False)
    return render(request,'myapp/allblogs.html',{'blog_posts':allblogs})

def mental(request):
    mental = BlogPost.objects.filter(category=1,is_draft=False)
    return render(request,'myapp/mental.html',{'blog_posts':mental})

def Heart(request):
    heart = BlogPost.objects.filter(category=2,is_draft=False)
    return render(request,'myapp/heart.html',{'blog_posts':heart})

def Covid(request):
    covid = BlogPost.objects.filter(category=3,is_draft=False)
    return render(request,'myapp/covid.html',{'blog_posts':covid})

def Immune(request):
    immune = BlogPost.objects.filter(category=4,is_draft=False)
    return render(request,'myapp/immune.html',{'blog_posts':immune})

def Error(request):
    return render(request,'myapp/error.html')

def Home(request):  
    if request.user.is_authenticated:
        return redirect('error')
    return render(request,'myapp/home.html')

@login_required
def Doctor(request):
    user = request.user
    if not request.user.is_doctor:
        return redirect('unauthorized')
    appointments = Appointment.objects.filter(doctor=user,date__gte=datetime.now())
    has_upcoming_appointment = appointments
    print(appointments)
    return render(request,'myapp/doctor.html',{'has_upcoming_appointment':has_upcoming_appointment})

@login_required
def Patient(request):
    if not request.user.is_patient:
        return redirect('unauthorized')
    return render(request,'myapp/patient.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')

