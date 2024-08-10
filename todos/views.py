# todos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Todo
from .forms import ProjectForm, TodoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from github import Github  
import requests
from django.conf import settings



def root_view(request):
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'todos/register.html', {'form': form})


@login_required
def home(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'todos/home.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'todos/create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    todos = project.todos.all()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.project = project
            todo.save()
            return redirect('project_detail', pk=pk)
    else:
        form = TodoForm()
    return render(request, 'todos/project_detail.html', {'project': project, 'todos': todos, 'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'todos/edit_project.html', {'form': form})

@login_required
def edit_todo(request, project_pk, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project_pk)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/edit_todo.html', {'form': form})

@login_required
def delete_todo(request, project_pk, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    todo.delete()
    return redirect('project_detail', pk=project_pk)

@login_required
def export_gist(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todos = project.todos.all()

    content = f"# {project.title}\n\n"
    content += f"**Summary**: {todos.filter(status=True).count()} / {todos.count()} completed\n\n"

    pending = "\n".join([f"- [ ] {todo.description}" for todo in todos.filter(status=False)])
    completed = "\n".join([f"- [x] {todo.description}" for todo in todos.filter(status=True)])

    content += "## Pending Tasks\n" + (pending if pending else "None\n") + "\n\n"
    content += "## Completed Tasks\n" + (completed if completed else "None\n")

    gist_data = {
        "description": f"Gist for project {project.title}",
        "public": False,
        "files": {
            f"{project.title}.md": {
                "content": content
            }
        }
    }

    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}"
    }

    response = requests.post('https://api.github.com/gists', json=gist_data, headers=headers)

    if response.status_code == 201:
        return redirect(response.json()['html_url'])
    else:
        return redirect('project_detail', pk=project.id)