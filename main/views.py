from django.shortcuts import render


def index_page(request):
    context = {
        'page_name': 'Index page'
    }
    return render(request, 'pages/index.html', context)



