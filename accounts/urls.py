from django.conf import settings
from django.conf.urls.static import static
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
    path('lawyerdetail',views.LawyerDetail,name='detail'),
    path('lawyer_messages/', views.lawyer_messages, name='lawyer_messages'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('send_message/<int:receiver_id>/<int:conversation_id>/', views.send_message,
         name='send_message_with_conversation'),
    path('reply_message/<int:conversation_id>/', views.reply_message, name='reply_message'),
    path('conversation_detail/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('client_messages/', views.client_messages, name='client_messages'),
]
