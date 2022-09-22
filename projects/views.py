from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse  
from .models import Project , Tag
from .forms import ProjectForm , ReviewForm
from .utils import searchProjects , paginateProjects





def projects(request):
    projects , search_query = searchProjects(request)
    tags = Tag.objects.all()

    projects , custom_range = paginateProjects(request, projects, 6)

    context ={ 'projects':projects , 'tags':tags , 'search_query':search_query , 'custom_range':custom_range}
    return render(request , 'projects/projects.html' , context)


def project(request, pk):
   projectObj = Project.objects.get(id=pk)
   tags = projectObj.tags.all()
   form = ReviewForm()
   if request.method =="POST":
    form = ReviewForm(request.POST)
    review = form.save(commit=False)
    review.project = projectObj
    review.owner = request.user.profile
    review.save()
    
    projectObj.getVoteCount

    messages.success(request, 'Review Added ')
    return redirect('project', pk = projectObj.id)
   return render(request , 'projects/single-project.html' , {'projectObj': projectObj , 'tags':tags ,'form':form} )

@login_required(login_url = "login")
def createProject(request):
    page = 'CreateProject'
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
           project=form.save(commit=False)
           project.owner = profile
           project.save()
           messages.success(request , 'Project Created Successfully ')
           return redirect('account')

    context ={'form':form ,'page':page}
    return render(request , 'projects/project-form.html' , context) 

@login_required(login_url = "login")
def updateProject(request , pk):
    page = 'EditProject'
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method=='POST':
        form = ProjectForm(request.POST, request.FILES , instance = project)
        if form.is_valid():
            form.save()
            messages.success(request , 'Project Updated Successfully ')
            return redirect('account')
    context = {'form':form , 'page':page}
    return render(request , 'projects/project-form.html' , context)

@login_required(login_url = "login")
def deleteProject(request , pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method =='POST':
        project.delete()
        messages.success(request , 'Project Deleted ')
        return redirect('account')
    context = {'object': project}
    return render(request , 'delete-template.html', context)