"""codetest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: fr3om django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from workspace.views import workspace, prep_files, send_files, ide_user, completed, reopen_workspace

app_name = 'workspace'
urlpatterns = [
    path('', workspace, name='my-workspace'),
    path('ide-user/', ide_user, name='ide-user'),
    path('prepare-files/', prep_files, name='prepare-files'),
    path('send-files/', send_files, name='send-files'),
    path('completed/', completed, name='completed'),
    path('reopen_workspace/', reopen_workspace, name='reopen_workspace'),
]
