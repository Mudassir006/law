from django.contrib import admin
from .models import User, Client, Lawyer

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Lawyer)
