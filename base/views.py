from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from in_for_a_penny.constants import GET
from .constants import THIS_APP


def get_landing(request: HttpRequest) -> HttpResponse:
    """
    Render landing page
    :param request: request
    :return: response
    """
    return get_home(request) if request.user.is_authenticated else render(
        request, f'{THIS_APP}/landing.html',context={
        })

@login_required
@require_http_methods([GET])
def get_home(request: HttpRequest) -> HttpResponse:
    """
    Render home page
    :param request: request
    :return: response
    """
    return render(request, f'{THIS_APP}/home.html',
                  context={
                  })


def get_about(request: HttpRequest) -> HttpResponse:
    """
    Render home page
    :param request: request
    :return: response
    """
    return render(request, f'{THIS_APP}/about.html',
                  context={
                  })


def get_links(request: HttpRequest) -> HttpResponse:
    """
    Render home page
    :param request: request
    :return: response
    """
    return render(request, f'{THIS_APP}/links.html',
                  context={
                  })
