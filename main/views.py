from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Hobby, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Rania Tsabitah Firsa",
        "nickname": "Naea",
        "npm": "2506616693",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Certified daydreamer. Living proof that you can major in something "
            "longer than planned while keeping your sanity intact."
        ),
    }
    return render(request, "index.html", context)


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

def show_projects(request):
    context = {
        "name": "Rania Tsabitah Firsa",
        "project_list": Project.objects.all(),
    }
    return render(request, "show_projects.html", context) 


def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
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
    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")