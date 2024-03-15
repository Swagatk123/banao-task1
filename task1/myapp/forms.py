from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,BlogPost,Category

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control'})
    )
    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs={'class':'form-control'})
    )
    
class SignUpForm(UserCreationForm):

    username = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control'})
    )
    first_name = forms.CharField(
            widget= forms.TextInput(
                attrs={'class':'form-control'})
    )
    last_name = forms.CharField(
            widget= forms.TextInput(
                attrs={'class':'form-control'})
    )
   
    email = forms.EmailField(
        widget= forms.EmailInput(
            attrs={'class':'form-control'})
    )
    password1 = forms.CharField(label='Password',
        widget= forms.PasswordInput(
            attrs={'class':'form-control'})
    )
    password2 = forms.CharField(label='Confirm Password (again)',
        widget= forms.PasswordInput(
            attrs={'class':'form-control'})
    )
    
    profile_picture = forms.ImageField(
        label="Upload Profile Photo",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    address = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control'})
    )
    city = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control'})
    )
    state = forms.Select(
    )
    pincode = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'form-control'})
    )
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2','is_doctor','is_patient','profile_picture','address','city','state','pincode')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']
        labels = {'image':'Upload Image',}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'image' :forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=Category.CATEGORY_CHOICES),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AppointmentForm(forms.Form):
    required_speciality = forms.CharField(max_length=100)
    date_of_appointment = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time_of_appointment = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))