from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms import NumberInput

from .models import User, Client, Lawyer
c = [('male','Male'),('female','Female'),('other','Other')]

class ClientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.image = self.cleaned_data.get('image')
        user.save()
        client = Client.objects.create(user=user)
        client.phone_number = self.cleaned_data.get('phone_number')
        client.location = self.cleaned_data.get('location')
        client.save()
        return user


class LawyerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    house_number = forms.CharField(required=True)
    area = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    cnic = forms.CharField(required=True,widget=NumberInput(attrs={'placeholder':'12345-1234567-1'}))
    date_of_birth = forms.DateField(required=True,widget=NumberInput(attrs={'type':'date'}))
    marital_status = forms.CharField(required=True)
    gender = forms.ChoiceField(required=True,choices=c)
    qualification = forms.CharField(required=True)
    university = forms.CharField(required=True)
    degree_start_from = forms.DateField(required=True,widget=NumberInput(attrs={'type':'date'}))
    degree_end = forms.DateField(required=True,widget=NumberInput(attrs={'type':'date'}))
    practice = forms.CharField(required=True)
    bar_council = forms.CharField(required=True)
    enrolment_year = forms.CharField(required=True)
    license_number = forms.CharField(required=True)
    current_firm = forms.CharField(required=True)
    Expertise = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lawyer = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.image = self.cleaned_data.get('image')
        user.save()
        lawyer = Lawyer.objects.create(user=user)
        lawyer.phone_number = self.cleaned_data.get('phone_number')
        lawyer.designation = self.cleaned_data.get('designation')

        lawyer.house_number = self.cleaned_data.get('house_number')
        lawyer.area = self.cleaned_data.get('area')
        lawyer.city = self.cleaned_data.get('city')
        lawyer.state = self.cleaned_data.get('state')
        lawyer.postal_code = self.cleaned_data.get('postal_code')
        lawyer.cnic = self.cleaned_data.get('cnic')
        lawyer.date_of_birth = self.cleaned_data.get('date_of_birth')
        lawyer.marital_status = self.cleaned_data.get('marital_status')
        lawyer.gender = self.cleaned_data.get('gender')
        lawyer.qualification = self.cleaned_data.get('qualification')
        lawyer.university = self.cleaned_data.get('university')
        lawyer.degree_start_from = self.cleaned_data.get('degree_start_from')
        lawyer.degree_end = self.cleaned_data.get('degree_end')
        lawyer.practice = self.cleaned_data.get('practice')
        lawyer.bar_council = self.cleaned_data.get('bar_council')
        lawyer.enrolment_year = self.cleaned_data.get('enrolment_year')
        lawyer.license_number = self.cleaned_data.get('license_number')
        lawyer.current_firm = self.cleaned_data.get('current_firm')
        lawyer.Expertise = self.cleaned_data.get('Expertise')

        lawyer.save()
        return user
