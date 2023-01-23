#  MIT License
#
#  Copyright (c) 2022-2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

"""soapbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from in_for_a_penny.constants import (
    LANDING_ROUTE_NAME, HOME_URL, HOME_ROUTE_NAME,
    ABOUT_URL, ABOUT_ROUTE_NAME, LINKS_URL, LINKS_ROUTE_NAME,
    CONVERT_URL, CONVERT_ROUTE_NAME, WEATHER_URL, WEATHER_ROUTE_NAME,
)
from .constants import THIS_APP
from .views import get_landing, get_home, get_about, get_links, get_convert, get_weather


# https://docs.djangoproject.com/en/4.1/topics/http/urls/#url-namespaces-and-included-urlconfs
app_name = THIS_APP


urlpatterns = [
    path(LINKS_URL, get_links, name=LINKS_ROUTE_NAME),
    path(ABOUT_URL, get_about, name=ABOUT_ROUTE_NAME),
    path(CONVERT_URL, get_convert, name=CONVERT_ROUTE_NAME),
    path(WEATHER_URL, get_weather, name=WEATHER_ROUTE_NAME),
    path('', get_landing, name=LANDING_ROUTE_NAME),
    path('', get_landing, name=HOME_ROUTE_NAME),
]
