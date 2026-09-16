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
        "project_list": Project.objects.all(),
    }
    return render(request, "show_projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_projects') 
    context = {'form': form}
    return render(request, 'project_form.html', context)