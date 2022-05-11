"""projectt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from projects.views import *
from django.conf.urls.static import static
from django.conf import settings
from crowdFunding.views import login, home, edit, delete,signup, activate, mylogout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',login,name='login'),
    path('home', home, name='home'),
    path('edit',edit, name='user_edit'),
    path('delete', delete, name='user_del'),
    path('', include('projects.urls')),
    path('signup/',signup , name = 'signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('logout',mylogout, name='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
