from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from olymp_prog.forms import TaskForm
from olymp_prog.models import Task, Training


@staff_member_required()
def main_page(request):
    context = {
        'page_name': 'Sports programming',
    }
    return render(request, 'pages/olymp_main.html', context)


@staff_member_required()
def add_task_page(request):
    task_form = None
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added')
            return redirect('olymp-add_task')
    context = {
        'page_name': 'Add task',
    }
    if task_form:
        context['add_task_form'] = task_form
    else:
        context['add_task_form'] = TaskForm()
    return render(request, 'pages/add_task.html', context)


@staff_member_required()
def tasks_catalog_page(request):
    context = {
        'page_name': 'Tasks catalog',
        'tasks': Task.objects.all()
    }
    return render(request, 'pages/tasks_catalog.html', context)


@staff_member_required()
def task_view_page(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    context = {
        'page_name': 'Task viewer',
        'task': task,
    }
    return render(request, 'pages/task_view.html', context)


@staff_member_required()
def training_page(request):
    try:
        training = Training.objects.get(user=request.user)
    except Training.DoesNotExist:
        return redirect('olymp-main')
    task = None
    if training.check_status('started'):
        task = training.get_current_task()
    context = {
        'page_name': 'Training',
        'status': training.get_status(),
    }
    if context['status'] == 'started':
        task.enable_nav_bar()
        context['current_task'] = task
    return render(request, 'pages/training.html', context)


@staff_member_required()
def start_new_training_page(request):
    context = {
        'page_name': 'Start new training',
    }
    return render(request, 'pages/start_new_training.html', context)
