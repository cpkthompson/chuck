import requests
from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from fabric2 import  Connection
from django.shortcuts import render
from decouple import config
# Create your views here.
from workspace.models import IdeUser


def workspace(request):
    workspaces = IdeUser.objects.all()
    workspace_current = ''
    for w in workspaces:
        workspace_current += w.workspace_name
    context = {
        'url': config('HOSTNAME'),
        'workspace_name': workspace_current
    }
    return render(request,'workspace/workspace.html', context=context)


def ide_user(request, workspace_name):
    my_workspace_name = workspace_name
    my_workspace = IdeUser.objects.create(workspace_name=my_workspace_name)
    return HttpResponse('OK')

def prep_files(request, container_name):
    host = config('MACHINE', default='MACHINE')
    pasw = config('PASW', default='PASW')
    root_image_name = config('ROOT_IMAGE_NAME', default='ROOT_IMAGE_NAME')
    connect = Connection(host=host)
    root_container_id = connect.local('echo {} | sudo -S docker ps | grep {}'.format(pasw, root_image_name)).stdout.rstrip()[0]
    connect.local('echo {} | sudo -S docker cp {}:/data/workspaces/{}/ ./{}'.format(pasw, root_container_id, container_name, container_name))
    ignore_dirs = ['.che', 'node_modules', '.pyc', 'venv']
    ignore_dir_string = ''
    for dir in ignore_dirs:
        ignore_dir_string = ignore_dir_string + " --exclude={}/{}".format(container_name, dir)
    connect.local("tar {} -czf {}.tar.gz {}/ -C .".format(ignore_dir_string, container_name, container_name))
    return HttpResponse('done')

def send_files(request, container_name, candidate_name):
    container_zip = "./{}.tar.gz".format((container_name))
    JENKINS_PATH = config('JENKINS_PATH', default='JENKINS_PATH')
    JENKINS_IP = config('JENKINS_IP', default='JENKINS_IP')
    JENKINS_PORT = config('JENKINS_PORT', default='JENKINS_PORT', cast=int)
    JENKINS_USER = config('JENKINS_USER', default='JENKINS_USER')
    JENKINS_PASW = config('JENKINS_PASW', default='JENKINS_PASW')
    JENKINS_TOKEN = config('JENKINS_TOKEN', default='JENKINS_TOKEN')
    JENKINS_URL = config('JENKINS_URL', default='JENKINS_URL')
    JENKINS_USER_ID =config('JENKINS_USER_ID', default='JENKINS_USER_ID')
    c = Connection(JENKINS_IP, port=JENKINS_PORT, user=JENKINS_USER, connect_kwargs={'password': JENKINS_PASW})
    c.put(container_zip, remote=JENKINS_PATH)
    # # make call to jenkins to trigger build and shut down server
    res = requests.post("https://{}:{}@{}/job/copy_files_to_workspace/buildWithParameters?token={}&directory_name={}&candidate_name={}".
                        format(JENKINS_USER_ID, JENKINS_TOKEN, JENKINS_URL,
                               JENKINS_TOKEN, container_name, candidate_name ))
    return HttpResponse('OK')