from django.urls import path
from .views import *
app_name = "projects"
urlpatterns = [
    path('', index),
    path("index", index, name="index"),
    path("categorie/<int:cid>", view, name="show"),
    path("search", search, name="search"),
    path("details/<int:pid>", details, name="detail"),
    path('mydonations/',my_donations,name='mydonations'),
    
    path('projects/',ProjectsList.as_view(),name="projects"),
    path('addproject/',add_project,name="add-project"),
    path('project/<int:pk>',ProjectDetail.as_view(),name="project"),
    path('addcomment/<project_id>',add_comment,name="addcomment"),
    # path('donate/<project_id>',add_donations,name="add-donation"),
    path('updateproject/<int:project_id>',editproject,name="editproject"),
    path('deleteproject/<int:project_id>',deleteproject,name="deleteproject"),
    path('myprojects/',my_projects,name='myprojects'),
    path("report/<int:pid>", reportproject, name="reportproject"),    # hadeer
    path("comment/<int:pid>", reportcomment, name="reportcomment"),    # hadeer
    path("donate/<int:pid>", donate, name="donate"),    # hadeer
    path("rate/<int:pid>", rate, name="rate"),    # hadeer
    
]
