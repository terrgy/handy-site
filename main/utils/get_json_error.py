from django.http import JsonResponse

from main.utils.get_json_response import get_json_response


def get_json_error(request, serv_messages=True, **kwargs) -> JsonResponse:
    return get_json_response(request, 'error', serv_messages=serv_messages, **kwargs)
