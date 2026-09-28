import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from .models import Project
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect


from main.models import Experience, Hobby, Project, Education
from main.forms import ProjectForm, EducationForm


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rania Tsabitah Firsa",
        "nickname": "Naea",
        "npm": "2506616693",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Certified daydreamer. Living proof that you can major in something "
            "longer than planned while keeping your sanity intact."
            ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    context = {
        "name": "Rania Tsabitah Firsa",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


def show_experience(request):
    context = {
        "name": "Rania Tsabitah Firsa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_hobbies(request):
    context = {
        "name": "Rania Tsabitah Firsa",  
        "hobby_list": Hobby.objects.all(),
    }
    return render(request, "hobbies.html", context)

def show_project(request):
    context = {
        "name": "Rania Tsabitah Firsa",
        "project_list": Project.objects.all(),
    }
    return render(request, "show_project.html", context) 


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")
        
    context = {
        "name": "Rania Tsabitah Firsa",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


def show_education(request):
    education_list = Education.objects.all()
    context = {
        'name': 'Rania Tsabitah Firsa',
        'education_list': education_list,
    }
    return render(request, 'show_education.html', context)

def add_education(request):
    form = EducationForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_education')
    context = {'form': form}
    return render(request, 'education_form.html', context)

def edit_education(request, id):
    education = get_object_or_404(Education, pk=id)
    form = EducationForm(request.POST or None, instance=education)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_education')
    context = {'form': form}
    return render(request, 'education_form.html', context)

def delete_education(request, id):
    education = get_object_or_404(Education, pk=id)
    education.delete()
    return HttpResponseRedirect('/education/')

def show_json(request):
    data = Education.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
    return redirect("main:show_projects")