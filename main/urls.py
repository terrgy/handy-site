from django.contrib.auth import views as auth_views
from django.urls import path, include

from main import views as main_views

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

# url - /fuck-off/...
fuck_off_urls = [
    path('', main_views.fuck_off, name='fuck_off_page'),
    path('ru/', main_views.fuck_off_ru, name='fuck_off_ru_page'),
]

main_urls = [
    path('', main_views.index_page, name='index'),
    path('auth/', include(auth_urls)),
    path('fuck-off/', include(fuck_off_urls)),
]
