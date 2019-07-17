import datetime

import requests
import pytz
from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from fabric2 import Connection

# Create your views here.
from workspace.models import IdeUser


def convert_time(seconds):
    days = int(seconds // (3600 * 24))
    hours = int((seconds // 3600) % 24)
    minutes = int((seconds // 60) % 60)
    seconds = int(seconds % 60)
    return '{} hrs : {} min : {} sec'.format(hours, minutes, seconds)


def workspace(request):
    workspacem = IdeUser.objects.all()[0]
    workspace_current = workspacem.workspace_name
    time = workspacem.end_time - datetime.datetime.now(tz=datetime.timezone.utc)
    workspace_end_time = convert_time(time.total_seconds())
    complete = workspacem.finished
    url = workspacem.url

    context = {
        'url': url,
        'workspace_name': workspace_current,
        'workspace_end_time': workspace_end_time,
        'completed': complete,
    }
    return render(request, 'workspace/workspace.html', context=context)

def ide_user(request):
    my_workspace_name = request.GET.get('workspace_name')
    time = request.GET.get('time')
    url = request.GET.get('url')
    fine_url = "http://{}".format(url)
    my_time = datetime.datetime.fromtimestamp(float(time))
    my_workspace = IdeUser.objects.create(workspace_name=my_workspace_name, end_time=my_time, url=fine_url)
    return HttpResponse('OK')


def prep_files(request):
    container_name = request.GET.get('container_name')
    host = config('MACHINE', default='MACHINE')
    pasw = config('PASW', default='PASW')
    root_image_name = config('ROOT_IMAGE_NAME', default='ROOT_IMAGE_NAME')
    connect = Connection(host=host)
    root_container_id = \
    connect.local('echo {} | sudo -S docker ps | grep {}'.format(pasw, root_image_name)).stdout.rstrip()[0]
    connect.local(
        'echo {} | sudo -S docker cp {}:/data/workspaces/{}/ ./{}'.format(pasw, root_container_id, container_name,
                                                                          container_name))
    ignore_dirs = ['.che', 'node_modules', '.pyc', 'venv', '.git', '.idea', '.gitignore']
    ignore_dir_string = ''
    for dir in ignore_dirs:
        ignore_dir_string = ignore_dir_string + " --exclude={}/{}".format(container_name, dir)
    connect.local("tar {} -czf {}.tar.gz {}/ -C .".format(ignore_dir_string, container_name, container_name))
    return HttpResponse('done')


def send_files(request):
    container_name = request.GET.get('container_name')
    candidate_name = request.GET.get('candidate_name')
    project_name = request.GET.get('project_name')
    company = request.GET.get('company')
    framework = request.GET.get('framework')
    name = "{}-{}".format(company.lower(), candidate_name.lower())
    container_zip = "./{}.tar.gz".format((container_name))
    JENKINS_PATH = config('JENKINS_PATH', default='JENKINS_PATH')
    JENKINS_IP = config('JENKINS_IP', default='JENKINS_IP')
    JENKINS_PORT = config('JENKINS_PORT', default='JENKINS_PORT', cast=int)
    JENKINS_USER = config('JENKINS_USER', default='JENKINS_USER')
    JENKINS_PASW = config('JENKINS_PASW', default='JENKINS_PASW')
    JENKINS_TOKEN = config('JENKINS_TOKEN', default='JENKINS_TOKEN')
    JENKINS_URL = config('JENKINS_URL', default='JENKINS_URL')
    JENKINS_USER_ID = config('JENKINS_USER_ID', default='JENKINS_USER_ID')
    c = Connection(JENKINS_IP, port=JENKINS_PORT, user=JENKINS_USER, connect_kwargs={'password': JENKINS_PASW})
    c.put(container_zip, remote=JENKINS_PATH)
    # # make call to jenkins to trigger build and shut down server


    resp1 = requests.post(
        "https://{}:{}@{}/createItem?name={}&mode=copy&from={}".format(JENKINS_USER_ID,JENKINS_TOKEN,JENKINS_URL,name,
                                                                  framework))
    if resp1.status_code in [201, 200]:
        res = requests.post('https://{}:{}@{}/job/{}/disable'.format(JENKINS_USER_ID, JENKINS_TOKEN,JENKINS_URL,name))
        res1 = requests.post('https://{}:{}@{}/job/{}/enable'.format(JENKINS_USER_ID, JENKINS_TOKEN,JENKINS_URL,name))
        res2 = requests.post(
            "https://{}:{}@{}/job/{}/buildWithParameters?token={}&directory_name={}&candidate_name={}"
            "&project_name={}".format(JENKINS_USER_ID, JENKINS_TOKEN, JENKINS_URL,name, JENKINS_TOKEN, container_name,
                                      name, project_name))
        return HttpResponse('OK')

def completed(request):
    workspacem = IdeUser.objects.all()[0]
    workspace_current = workspacem.workspace_name
    time = workspacem.end_time - datetime.datetime.now(tz=datetime.timezone.utc)
    workspace_end_time = convert_time(time.total_seconds())
    workspacem.finished = True
    complete = workspacem.finished
    workspacem.save()
    url = workspacem.url


    context = {
        'url': url,
        'workspace_name': workspace_current,
        'workspace_end_time': workspace_end_time,
        'completed': complete,
    }
    return render(request, 'workspace/workspace.html', context=context)
