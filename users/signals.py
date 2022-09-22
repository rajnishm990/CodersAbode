from django.db.models.signals import post_save , post_delete 
from .models import Profile 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
#from django.dispatch import reciever 


#Singals are certain actions that get triggered after an event occurs . For exampe if a user is is saved in our database and we
# have to make a profile for that user , we can simply make a function using signals that would make a profile of the registered
# user automatiaclly. 
# post_save means that this events fires after something is saved (like a user , or a project)
# post_delete means that this events fires after somethign is deleted 
#It is necessary to connect this new singal file to our main app by going into app.py and writing a function named ready 
# that takes self as argument and imports users.signals  def(self): import users.singals  . Inside tha class UsersConfig

def createProfile(sender, instance , created , **kwargs):   
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        subject = 'Welcome To Coders Abode'
        body = 'Your CodersAbode Account has been succesfully created . We are glad to have you on our platoform'

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently= False
        )


def updateProfile(sender , instance , created , **kwargs):
    profile = instance
    user= profile.user

    if created ==False:
        user.first_name =profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()

def deleteUser(sender , instance , **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender = User)  #connecting signals to the event 
post_save.connect(updateProfile , sender =Profile)
post_delete.connect(deleteUser , sender=Profile)