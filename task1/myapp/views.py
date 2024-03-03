from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
def Index(request):
    return render(request,'myapp/base.html')

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

def Error(request):
    return render(request,'myapp/error.html')

def Home(request):  
    if request.user.is_authenticated:
        return redirect('error')
    return render(request,'myapp/home.html')

@login_required
def Doctor(request):
    return render(request,'myapp/doctor.html')

@login_required
def Patient(request):
    return render(request,'myapp/patient.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')

