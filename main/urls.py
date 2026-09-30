from django.urls import path

from main.views import (
    show_main, 
    show_experience, 
    create_project, 
    create_project_ajax,
    show_project, 
    get_projects_json, 
    edit_project,      
    delete_project,    
    show_education, 
    add_education, 
    edit_education, 
    delete_education, 
    show_json, 
    register, 
    login_user, 
    logout_user, 
    toggle_star
) 

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_project, name="show_project"), 
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/edit/<uuid:id>/", edit_project, name="edit_project"),       # Ditambahkan
    path("projects/delete/<uuid:id>/", delete_project, name="delete_project"), # Ditambahkan
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path('education/', show_education, name='show_education'),
    path('education/add/', add_education, name='add_education'),
    path('education/edit/<int:id>/', edit_education, name='edit_education'),
    path('education/delete/<int:id>/', delete_education, name='delete_education'),
    path('education/json/', show_json, name='show_json'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('projects/<uuid:project_id>/star/', toggle_star, name='toggle_star'),
]