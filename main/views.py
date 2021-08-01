from django.shortcuts import render, redirect


def index_page(request):
    return redirect('fuck_off_page')


def fuck_off(request):
    context = {
        'page_name': 'Fuck off'
    }
    return render(request, 'pages/fuck_off.html', context)


def fuck_off_ru(request):
    context = {
        'page_name': 'Съебись'
    }
    return render(request, 'pages/fuck_off_ru.html', context)


