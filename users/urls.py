from django.urls import path
from . import views

urlpatterns =[
    path('login/' , views.loginUser , name='login'),
    path('register/' , views.registerUser , name='register'),
    path('logout/', views.logoutUser , name = 'logout'),
    path('account/' , views.userAccount , name ='account'),
    path('edit-account/' ,views.editAccount , name ='editAccount'),
    path('' , views.profiles , name ='profiles' ),
    path('profile/<str:pk>', views.profile, name ="profile"),
    path('create-skill/' , views.createSkill , name ='createSkill'),
    path('update-skill/<str:pk>/' , views.updateSkill , name ='updateSkill'),
    path('delete-skill/<str:pk>/' , views.deleteSkill , name ='deleteSkill'),
    path('inbox/' , views.inbox , name='inbox'),
    path('message/<str:pk>', views.viewMessage , name = 'message'),
    path('create-message/<str:pk>', views.createMessage , name='createMessage'),

]