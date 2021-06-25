from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from olymp_prog.forms import TaskForm, TaskFilterForm, TrainingSettings
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
    if request.method == 'POST':
        task_filter_form = TaskFilterForm(request.POST)
        if not task_filter_form.is_valid():
            task_filter_form = TaskFilterForm()
    else:
        task_filter_form = TaskFilterForm()
    try:
        tasks = Task.filter_tasks(**task_filter_form.cleaned_data)
    except AttributeError:
        tasks = Task.filter_tasks()
    context = {
        'page_name': 'Tasks catalog',
        'tasks': tasks,
        'task_filter_form': task_filter_form,
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
def task_edit_page(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        edit_form = TaskForm(request.POST, instance=task)
        if edit_form.is_valid():
            edit_form.save()
            edit_form = TaskForm(instance=task)
    else:
        edit_form = TaskForm(instance=task)

    context = {
        'page_name': 'Task edit',
        'task': task,
        'edit_form': edit_form,
    }
    return render(request, 'pages/task_edit.html', context)


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
    if request.method == 'POST':
        settings_form = TrainingSettings(request.POST)
        if settings_form.is_valid():
            tasks = Task.filter_tasks(**settings_form.cleaned_data)
            tasks = Task.get_shuffle_method(int(settings_form.cleaned_data['shuffle_method']))(tasks)
            Training.start_new_training(request, tasks)
            return redirect('olymp-training')
    else:
        settings_form = TrainingSettings()
    context = {
        'page_name': 'Start new training',
        'settings_form': settings_form,
    }
    return render(request, 'pages/start_new_training.html', context)
