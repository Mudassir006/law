from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('client_register', views.client_register.as_view(), name='client_register'),
    path('lawyer_register/', views.lawyer_register.as_view(), name='lawyer_register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.base, name='home'),
    path('lawhome', views.main, name='lawhome'),
    path('clienthome', views.clienthome, name='clienthome'),
    path('lawyerdetail',views.LawyerDetail,name='detail')
]
