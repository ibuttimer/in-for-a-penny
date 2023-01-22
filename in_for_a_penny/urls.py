"""in_for_a_penny URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from in_for_a_penny import settings
from .constants import BASE_APP_NAME, ADMIN_URL, ACCOUNTS_URL, BUDGET_URL

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),

    path(BUDGET_URL, include('budget.urls')),

    path(ACCOUNTS_URL, include('allauth.urls')),

    path('', include(f'{BASE_APP_NAME}.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
