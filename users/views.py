from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile , Message
from projects.models import Project
from django.contrib.auth import login , logout , authenticate
from .forms import CustomUserCreationForm , ProfileForm , skillForm , messageForm
from .utils import searchProfiles , paginateProfiles


def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print('Username does not exist')
        
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else :
            messages.error(request , 'Username or Password Incorrect')

        
    return render(request , 'users/login_register.html')

def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    
    if request.method =='POST':
        form  = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request , 'Profile Created successfully ')
            login(request , user)
            return redirect('profiles')
            
        else:
            messages.error(request , "Something went wrong during registration")
    
    context ={'page': page , 'form': form}
    return render(request  , 'users/login_register.html' , context)

def logoutUser(request):
    logout(request)
    messages.info(request , "User Logged Out sucessfully ")
    return redirect('login')



def profiles(request):
    profiles , search_query = searchProfiles(request)

    profiles , custom_range= paginateProfiles(request, profiles, 6)
    context ={'profiles': profiles , 'search_query': search_query, 'custom_range':custom_range}
    return render(request , 'users/profiles.html' , context)

def profile(request , pk):
    profile = Profile.objects.get(id=pk)
    #projects =Project.objects.get(owner = user)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context={'profile':profile , 'topSkills': topSkills , 'otherSkills':otherSkills }
    return render(request, 'users/single-profile.html', context) 

@login_required(login_url ='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context ={'profile': profile ,'skills':skills}
    return render(request , 'users/account.html' , context)

@login_required(login_url = 'login')
def editAccount(request):
    
    profile = request.user.profile
    form = ProfileForm(instance =profile)
    if request.method =="POST":
        form = ProfileForm(request.POST , request.FILES , instance = profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request , 'users/profile_form.html', context)

@login_required(login_url = 'login')
def createSkill(request):
    profile = request.user.profile
    form = skillForm()
    if request.method=='POST':
        form  = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit =False)
            skill.owner = profile
            skill.save()
            messages.success(request , 'Skill was Added ')
            return redirect('account')
    context = {'form':form}
    return render(request , 'users/skill_form.html' , context)

@login_required(login_url='login')
def updateSkill(request , pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = skillForm(instance = skill)
    if request.method == 'POST':
        form = skillForm(request.POST , instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request , 'Skill was Udated ')
            return redirect('account')

    context={'form':form}
    return render(request , 'users/skill_form.html' , context)

@login_required(login_url='login')
def deleteSkill(request , pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request , 'Skill Deleted ')
        return redirect('account')
    context = {'object': skill}
    return render(request , 'delete-template.html' , context)
        
@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    messageObj = profile.messages.all()
    unread_count = messageObj.filter(is_read=False).count()
    context={'messageObj':messageObj , 'unread_count':unread_count}
    return render (request , 'users/inbox.html', context)

@login_required(login_url = 'login')
def viewMessage(request , pk):
    profile = request.user.profile
    messageObj = profile.messages.get(id=pk)
    if messageObj.is_read==False:
        messageObj.is_read=True
        messageObj.save()
    context = {'messageObj':messageObj}
    return render(request, 'users/message.html' , context)

def createMessage(request , pk):
    recepient = Profile.objects.get(id=pk)
    form = messageForm()

    try:
        sender = request.user.profile
    except:
        sender=None

    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.reciepent= recepient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request , 'Message Sent Succesfully')
            return redirect('profile' , pk=recepient.id)
    
    context={'recepient': recepient , 'form':form}
    return render(request , 'users/message_form.html', context)