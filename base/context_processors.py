
from django.http import HttpRequest

from in_for_a_penny.constants import APP_NAME
from .constants import APP_NAME_CTX


def base_context(request: HttpRequest) -> dict:
    """
    Add base-specific context entries
    :param request: http request
    :return: dictionary to add to template context
    """
    context = {
        APP_NAME_CTX: APP_NAME
    }
    return context
