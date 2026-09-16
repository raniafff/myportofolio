from django.urls import path

from main.views import show_main, show_experience, show_hobbies, create_project, show_projects 

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('hobbies/', show_hobbies, name='show_hobbies'),
    path("projects/", show_projects, name="show_projects"), 
    path("projects/add/", create_project, name="create_project"),
]