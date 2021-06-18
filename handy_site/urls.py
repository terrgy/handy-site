"""handy_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main import views as main_views
from olymp_prog import views as olymp_views, ajax_views as olymp_ajax_views
from django.contrib.auth import views as auth_views

# url - /olymp/task/<task_id>/...
task_urls = [
    path('', olymp_views.task_view_page, name='olymp-task_view'),
    path('solve/', olymp_ajax_views.solve_task_request, name='olymp-solve_task'),
    path('try-to-solve-task', olymp_ajax_views.try_to_solve_task_request, name='olymp-try_to_solve_task'),
]

# url - /olymp/ajax/...
olymp_ajax_urls = [
    path('start-training/', olymp_ajax_views.start_training_request, name='olymp-start_training'),
    path('end-training/', olymp_ajax_views.end_training_request, name='olymp-end_training'),
    path('next-task/', olymp_ajax_views.next_task_request, name='olymp-next_task'),
    path('add-tag/', olymp_ajax_views.add_tag_request, name='olymp-add_tag'),
    path('delete-tag/', olymp_ajax_views.delete_tag_request, name='olymp-delete_tag'),
    path('get-tags/', olymp_ajax_views.get_tags_request, name='olymp-get_tags'),
]

# url - /olymp/...
olymp_urls = [
    path('', olymp_views.main_page, name='olymp-main'),
    path('add-task/', olymp_views.add_task_page, name='olymp-add_task'),
    path('tasks-catalog/', olymp_views.tasks_catalog_page, name='olymp-tasks_catalog'),
    path('task/<int:task_id>/', include(task_urls)),
    path('training/', olymp_views.training_page, name='olymp-training'),
    path('start-new-training', olymp_views.start_new_training_page, name='olymp-start_new_training_page'),
    path('ajax/', include(olymp_ajax_urls)),
]

# url - /auth/...
auth_urls = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'page_name': 'Авторизация'
            },
            template_name='auth/login.html'
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index_page, name='index'),
    path('olymp/', include(olymp_urls)),
    path('auth/', include(auth_urls)),
]
