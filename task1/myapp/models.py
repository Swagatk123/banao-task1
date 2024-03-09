from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
STATE_CHOICES = (
  ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
  ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
  ('Assam','Assam'),
  ('Bihar','Bihar'),
  ('Chandigarh','Chandigarh'),
  ('Chhattisgarh','Chhattisgarh'),
  ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
  ('Daman and Diu','Daman and Diu'),
  ('Delhi','Delhi'),
  ('Goa','Goa'),
  ('Gujarat','Gujarat'),
  ('Haryana','Haryana'),
  ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu & Kashmir','Jammu & Kashmir'),
  ('Jharkhand','Jharkhand'),
  ('Karnataka','Karnataka'),
  ('Kerala','Kerala'),
  ('Lakshadweep','Lakshadweep'),
  ('Madhya Pradesh','Madhya Pradesh'),
  ('Maharashtra','Maharashtra'),
  ('Manipur','Manipur'),
  ('Meghalaya','Meghalaya'),
  ('Mizoram','Mizoram'),
  ('Nagaland','Nagaland'),
  ('Odisha','Odisha'),
  ('Puducherry','Puducherry'),
  ('Punjab','Punjab'),
  ('Rajasthan','Rajasthan'),
  ('Sikkim','Sikkim'),
  ('Tamil Nadu','Tamil Nadu'),
  ('Telangana','Telangana'),
  ('Tripura','Tripura'),
  ('Uttarakhand','Uttarakhand'),
  ('Uttar Pradesh','Uttar Pradesh'),
  ('West Bengal','West Bengal'),
)
class User(AbstractUser):
    is_doctor = models.BooleanField('Is Doctor',default=False)
    is_patient = models.BooleanField('Is Patient',default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=50,blank=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=50,blank=True)
    pincode = models.CharField(max_length=10,blank=True)

class Category(models.Model):
    MENTAL_HEALTH = 'Mental Health'
    HEART_DISEASE = 'Heart Disease'
    COVID_19 = 'Covid19'
    IMMUNIZATION = 'Immunization'

    CATEGORY_CHOICES = [
        (MENTAL_HEALTH, 'Mental Health'),
        (HEART_DISEASE, 'Heart Disease'),
        (COVID_19, 'Covid19'),
        (IMMUNIZATION, 'Immunization'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/',null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_draft = models.BooleanField('Is Draft',default=True)

    def __str__(self):
        return self.title
    
  