from django.db import models
import uuid 
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile , blank=True ,null=True , on_delete = models.SET_NULL)
    title= models.CharField(max_length = 200)
    description = models.TextField( null = True , blank=True)
    demo_link = models.CharField(max_length = 200 , null = True , blank = True)
    featured_image = models.ImageField(null=True , blank = True , default = "default.jpg")
    source_link = models.CharField(max_length = 200 , null = True , blank = True)
    tags = models.ManyToManyField('Tag' , blank =True)
    vote_total = models.IntegerField(default = 0 , null = True , blank =True)
    vote_ratio = models.IntegerField(default = 0 , null = True , blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4 ,unique = True , editable = False, primary_key = True )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['-vote_ratio' , '-vote_total' , 'title']

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        totalVotes= reviews.count()
        ratio = (upvotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

class Review(models.Model):
    VOTE_TYPE = (
        ('up' , 'up vote'),
        ('down ', 'down Vote'),
    )
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE , null=True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField(null=True , blank = True)
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add =True)
    id =models.UUIDField(default = uuid.uuid4,unique = True , editable = False, primary_key = True )

    class Meta:
        unique_together=[[ 'owner','project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name= models.CharField(max_length =200)
    created = models.DateTimeField(auto_now_add =True)
    id =models.UUIDField(default = uuid.uuid4,unique = True , editable = False, primary_key = True )
    
    def __str__(self):
        return self.name
