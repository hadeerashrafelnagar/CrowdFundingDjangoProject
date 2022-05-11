from django.shortcuts import render
from .forms import *
from .models import *
from django.urls import reverse_lazy
#from django.db.models import Avg
from django.shortcuts import get_object_or_404,redirect,render,HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView,DetailView,CreateView

# Create your views here.


# home views
#from projectt.crowdFunding import models
from crowdFunding.models import myuser


def index(request):
    projects = Project.objects.all()
    ProjectRate = Project.objects.annotate(avg=Avg("rate__rate")).order_by('avg')[:5]
    lastProject = Project.objects.order_by('id')[:5]
    featureProjects = FeatureProjects.objects.all()
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "ProjectRate": ProjectRate,
        "lastProject": lastProject,
        "featureProjects": featureProjects,
        "categories": categories
    }
    return render(request, "projects/projectHome.html", context)


def view(request, cid):
    projects = get_object_or_404(Categories, id=cid)
    categories = Categories.objects.all()
    context = {
        "projects": projects.project,
        "categories": categories,
        "categoryName": projects.name
    }

    return render(request, "projects/view.html", context)


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        mode = form.cleaned_data.get("mode")
        searching = form.cleaned_data.get("search")
        if mode == "1":
            projects = ProjectTage.objects.filter(tage=searching)
            if projects:
                projects = projects[0].project_all()
        else:
            projects = Project.objects.filter(title=searching)
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "categories": categories,
        "categieName": searching
    }
    return render(request, "projects/view.html", context)


def details(request, pid):
    categories = Categories.objects.all()
    authenticated=None
    owned=None
    project = get_object_or_404(Project, id=pid)
    if 'Email' in request.session :
             if myuser.objects.get(Email=request.session['Email'])==project.user:
                 print("yes tnis is owner ", myuser.objects.get(Email=request.session['Email']))
                 owned=True
             else :
                 authenticated=myuser.objects.get(Email=request.session['Email'])
             
             
            
    else:
            authenticated=None
            owned=None

    context = {
        "categories": categories,
        "images": project.allImage(),
        "project": project,
        "relativesProject": project.relativeProject(),
        "commentcount": project.comments().count(),
        "owned":owned,
        "authenticated":authenticated
    }
    return render(request, "projects/details.html", context)



############################################################
class ProjectsList(ListView):
    template_name="projects/AllProjects.html"
    model=Project
    def get_query(self):
        return Project.objects.all()
   
    def get_context_data(self,**kwargs):
        if 'Email' in self.request.session :
             authenticated=myuser.objects.get(Email=self.request.session['Email'])
        else:
            authenticated=None
        context = super().get_context_data(**kwargs)
        context['authenticated'] = authenticated
        return context
       

class ProjectDetail(DetailView):
    model=Project
    template_name="projects/project.html"
    def get_context_data(self,**kwargs):
        if 'Email' in self.request.session :
             authenticated=myuser.objects.get(Email=self.request.session['Email'])
             owned=None
             if myuser.objects.get(Email=self.request.session['Email'])==self.object.user:
                 print("yes tnis is owner ", myuser.objects.get(Email=self.request.session['Email']))
                 owned=True
             else :
                 print("diffrent one ", myuser.objects.get(Email=self.request.session['Email']))
        else:
            authenticated=None
        context = super().get_context_data(**kwargs)
        context['authenticated'] = authenticated
        context['owned'] = owned
        return context
    
def deleteproject (req,project_id):
        obj=Project.objects.get(pk=project_id)
        obj.delete()
        return HttpResponseRedirect("/myprojects")
    
    
def add_comment (req,project_id):
     if req.method=="POST" :
         print(Project.objects.get(pk=project_id))
         comment=Comment.objects.create(user=myuser.objects.get(Email=req.session['Email']),
                                        project=Project.objects.get(pk=project_id), content=req.POST['content'])
     return HttpResponseRedirect(f"/details/{project_id}")
         
# def add_donations (req,project_id):
#      if req.method=="POST" :
#          print(Project.objects.get(pk=project_id))
#          donation=Donation.objects.create(owner=myuser.objects.get(Email=req.session['Email']),
#            project=Project.objects.get(pk=project_id),amount=req.POST['rate'])
#      return HttpResponseRedirect(f"/details/{project_id}")

def my_projects(req):
    list=Project.objects.filter(user=myuser.objects.get(Email=req.session['Email']))
    return render (req,'projects/profile.html',{'list':list})

class newForm(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/NewProject.html'
    success_url = reverse_lazy('projects')
    
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
        
    def form_valid(self, form): 
        obj = form.save(commit=False)
        obj.user = myuser.objects.get(Email=self.request.session['Email'])
        obj.save()        
        return HttpResponseRedirect(self.success_url)
    
    
    
def add_project(request):
    submitted=False
    if request.method=="GET" :
        # new form
        form=ProjectForm()
        if 'submitted' in request.GET :
            # from the 2nd second request
            submitted=True
        return render (request,'projects/NewProject.html',{'form':form,'submitted':submitted})
    else :
        #req is post data already in
        form=ProjectForm(request.POST,request.FILES)
        
        if form.is_valid():
            project=form.save(commit=False)
            project.user=myuser.objects.get(Email=request.session['Email'])
            if project.start_date >= project.end_date :
                print("YYYYYYYYYYYYYYYYYYY")
            project.save()
            return HttpResponseRedirect('/')
        else :
           return render (request,'projects/NewProject.html',{'form':form,'submitted':submitted})

def editproject(req,project_id):
    project=Project.objects.get(pk=project_id)
    form=ProjectForm(req.POST or None , instance=project)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(f"/details/{project_id}")
    return render(req,'projects/editProject.html',{'form':form,'project':project})



def reportproject(request, pid):
    form = ReportFormProject(request.POST)
    if form.is_valid():
        project = get_object_or_404(Project, id=pid)
        content = form.cleaned_data.get("content")
        ReportProject.objects.create(
            project=project, content=content, user=request.user)
        messages.success(request, "report sent")
        if ReportProject.objects.all().count() >= 6:
            project.delete()
            return HttpResponseRedirect("/")
    else:
        messages.error(request, "report unsent")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # hadeer


def reportcomment(request, pid):
    form = ReportFormComment(request.POST)
    if form.is_valid():
        comment = get_object_or_404(Comment, id=pid)
        content = form.cleaned_data.get("content")
        ReportComment.objects.create(
            comment=comment, content=content, user=request.user)
        messages.success(request, "report sent")
        if ReportComment.objects.all().count() >= 3:
            comment.delete()
            return HttpResponseRedirect("/")
    else:
        messages.error(request, "report unsent")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # hadeer


def donate(request, pid):
    form = DonationForm(request.POST)
    if form.is_valid():
        project = get_object_or_404(Project, id=pid)
        amount = form.cleaned_data.get("amount")
        Donation.objects.create(owner=myuser.objects.get(Email=request.session['Email']),
                                project=Project.objects.get(pk=pid), amount=request.POST['amount'])
        donate = project.donationMoney()
        if project.totalTarget == donate['amount__sum']:
            Project.objects.filter(id=pid).delete()
        return HttpResponseRedirect("/")
    # hadeer


def rate(request, pid):
    form = RatingForm(request.POST)
    if form.is_valid():
        project = get_object_or_404(Project, id=pid)
        rate = form.cleaned_data.get("rate")
        print(rate)
        print(Rate.objects.filter(user=myuser.objects.get(Email=request.session['Email'])).filter(
            project=Project.objects.filter(id=pid)[0]).count())
        print(Project.objects.filter(id=pid)[0])
        if Rate.objects.filter(user=myuser.objects.get(Email=request.session['Email'])).filter(project=Project.objects.filter(id=pid)[0]).count() < 1 and Project.objects.filter(id=pid)[0] == project:
            Rate.objects.create(
                project=project, rate=rate, user=myuser.objects.get(Email=request.session['Email']))
        else:
            messages.error(request, "you already rate this project")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # hadeer
def my_donations(req):
    list=Donation.objects.filter(owner=myuser.objects.get(Email=req.session['Email']))
    return render (req,'projects/donations.html',{'list':list})