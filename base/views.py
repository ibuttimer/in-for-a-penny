from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .constants import THIS_APP


def get_landing(request: HttpRequest) -> HttpResponse:
    """
    Render landing page
    :param request: request
    :return: response
    """
    return render(request, f'{THIS_APP}/landing.html',
                  context={
                  })
