from django.http import JsonResponse

from main.utils.render_messages import render_messages


def get_json_response(request, status='ok', serv_messages=True, **kwargs) -> JsonResponse:
    if serv_messages:
        return JsonResponse({
            'status': status,
            'messages': render_messages(request),
            **kwargs
        })
    return JsonResponse({
        'status': status,
        **kwargs
    })
