from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_lawyer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(null=True)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20)


class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)

    house_number = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    cnic = models.CharField(max_length=16)
    date_of_birth = models.CharField(max_length=19)
    marital_status = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    qualification = models.CharField(max_length=20)
    university = models.CharField(max_length=250)
    degree_start_from = models.CharField(max_length=14)
    degree_end = models.CharField(max_length=14)
    practice = models.CharField(max_length=50)
    bar_council = models.CharField(max_length=50)
    enrolment_year = models.CharField(max_length=14)
    license_number = models.CharField(max_length=10)
    current_firm = models.CharField(max_length=50)
    Expertise = models.CharField(max_length=20)


# models.py




class Conversation(models.Model):
    participants = models.ManyToManyField(User)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='message_files/', null=True, blank=True)