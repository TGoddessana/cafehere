from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework import status

from core.http.response import ResponseFormat


def server_error(request, *args, **kwargs):
    """
    Django's default 500 error handler.
    """
    data = ResponseFormat(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Server Error (500)",
        data=None,
    ).to_dict()
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def not_found(request: WSGIRequest, exception, *args, **kwargs):
    """
    Django's default 404 error handler.
    """
    data = ResponseFormat(
        code=status.HTTP_404_NOT_FOUND,
        message="Not Found (404)",
        data=None,
    ).to_dict()
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
