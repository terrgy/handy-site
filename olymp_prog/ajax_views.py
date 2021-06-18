from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse

from main.utils.get_json_error import get_json_error
from main.utils.get_json_response import get_json_response
from olymp_prog.models import Training, Task, Tag


@staff_member_required()
def start_training_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    Training.start_new_training(request)
    return get_json_response(request, redirect=reverse('olymp-training'))


@staff_member_required()
def next_task_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    training = get_object_or_404(Training, user=request.user)
    if not training.check_status('started'):
        messages.add_message(request, messages.ERROR, 'Invalid request')
        return get_json_error(request)
    training.next_task()
    return get_json_response(request, redirect=reverse('olymp-training'))


@staff_member_required()
def end_training_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    training = get_object_or_404(Training, user=request.user)
    if not training.check_status('started'):
        messages.add_message(request, messages.ERROR, 'Invalid request')
        return get_json_error(request)
    training.end_training()
    return get_json_response(request, reload='reload')


@staff_member_required()
def solve_task_request(request, task_id):
    if request.method != 'POST':
        raise PermissionDenied
    task = get_object_or_404(Task, pk=task_id)
    task.solve()
    return get_json_response(request, reload='reload')


@staff_member_required()
def try_to_solve_task_request(request, task_id):
    if request.method != 'POST':
        raise PermissionDenied
    task = get_object_or_404(Task, pk=task_id)
    task.try_to_solve()
    return get_json_response(request, reload='reload')


@staff_member_required()
def add_tag_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    tag_name = request.POST.get('tag-name')
    if tag_name is None:
        messages.add_message(request, messages.ERROR, 'Missing tag name')
        return get_json_error(request)
    if not tag_name:
        messages.add_message(request, messages.ERROR, 'Tag name can\'t be empty')
        return get_json_error(request)
    try:
        new_tag = Tag.objects.create(name=tag_name)
    except IntegrityError:
        messages.add_message(request, messages.ERROR, 'Tag with this name already exists')
        return get_json_error(request)
    new_tag_dict = {
        'name': new_tag.name,
        'value': new_tag.pk,
    }
    return get_json_response(request, new_tag=new_tag_dict)


@staff_member_required()
def delete_tag_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    tag_pk = request.POST.get('tag-value')
    if tag_pk is None:
        messages.add_message(request, messages.ERROR, 'Missing tag value')
        return get_json_error(request)
    if not tag_pk:
        messages.add_message(request, messages.ERROR, 'Tag value can\'t be empty')
        return get_json_error(request)
    try:
        tag = Tag.objects.get(pk=tag_pk)
        tag_value = tag.pk
        tag.delete()
    except Tag.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Tag does not exist')
        return get_json_error(request)
    return get_json_response(request, tag_value=tag_value)


@staff_member_required()
def get_tags_request(request):
    if request.method != 'POST':
        raise PermissionDenied
    return get_json_response(request, tags=Tag.get_all_tags_list())
