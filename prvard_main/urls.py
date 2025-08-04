from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_f, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_f, name='logout'),
    path('leave', views.leave, name='leave'),
    path('delete/<int:university_id>', views.delete, name='delete'),
    path('join', views.join, name='join'),
    path('Create_University', views.createu, name='createu'),
    path('Create/University/<str:Theme>', views.createu_f, name='createu_f'),
    path('mobile-blocked', views.mobile_blocked, name='mobile_blocked'),
    path('profile', views.profile, name='profile'),
    path('profile/<int:id>', views.profile_other, name='profile_o'),
    path('members', views.members, name='members'),
    path('message', views.send_message, name='message'),
    path('inbox', views.inbox, name='inbox'),
    path('send', views.send, name='send'),
    path('message/<int:message_id>', views.show_message, name='show'),
    path('delete/message/<int:message_id>', views.delete_m, name='delete_m'),
    path('classes/', views.all_classes, name='all_classes'),
    path('entroll/<int:id>', views.Entroll, name='entroll'),
    path('Create/Class', views.createC, name='createC'),
    path('Delete/User/<int:id>', views.Delete_u, name='delete_u'),
    path('Login/<int:id>', views.Oclass, name='Oclass'),
    path('Class/<int:id>', views.Open_Class, name='Opclass'),
    path('Leave/Class/<int:id>', views.leaveC, name='Lclass'),
    path('Delete/Class/<int:id>', views.DeleteC, name='Dclass'),
    path('Member/Class/<int:id>', views.Cmember, name='Mclass'),
    path('Create/Week/<int:id>', views.Cweek, name='Cweek'),
    path('Edit/Week/<int:id>', views.Eweek, name='Eweek'),
    path('Show/Week/<int:id>', views.ShowW, name='ShowW'),
    path('Chat/Class/<int:id>', views.Chat1, name='Cclass'),
    path('Add/Message/Class/<int:id>', views.add_message, name='ACclass'),
    path('Delete/Lesson/<int:id>', views.Delete_L, name='DWclass'),


]