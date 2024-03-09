from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm,BlogPostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BlogPost
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
    return render(request,'myapp/allblogs.html',{'blog_posts':allblogs,'Mental':mental})

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
    if not request.user.is_doctor:
        return redirect('unauthorized')
    return render(request,'myapp/doctor.html')

@login_required
def Patient(request):
    if not request.user.is_patient:
        return redirect('unauthorized')
    return render(request,'myapp/patient.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')

