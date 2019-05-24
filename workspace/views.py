import requests
from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from fabric.api import local
from fabric2 import  Connection
from django.shortcuts import render
from decouple import config
# Create your views here.

def workspace(request):

    context = {
        'url': config('HOSTNAME')
    }
    return render(request,'workspace/workspace.html', context=context)


def prep_files(request, container_name):
    host = config('MACHINE', default='MACHINE')
    command_var = config('COMMAND_VAR', default='COMMAND_VAR')
    root_image_name = config('ROOT_IMAGE_NAME', default='ROOT_IMAGE_NAME')
    connect = Connection(host=host)
    root_container_id = connect.local(f"sudo docker ps | grep {root_image_name} | awk '{command_var}'").stdout.rstrip()
    connect.local(f'sudo docker cp {root_container_id}:/data/workspaces/{container_name}/ ./{container_name}')
    ignore_dirs = ['.che', 'node_modules', '.pyc', 'venv']
    ignore_dir_string = ''
    for dir in ignore_dirs:
        ignore_dir_string = ignore_dir_string + f' --exclude={container_name}/{dir}'
    connect.local(f'tar {ignore_dir_string} -czf {container_name}.tar.gz {container_name}/ -C .')
    return HttpResponse('done')

def send_files(request, container_name):
    container_zip = f'./{container_name}.tar.gz'
    JENKINS_PATH = config('JENKINS_PATH', default='JENKINS_PATH')
    JENKINS_IP = config('JENKINS_IP', default='JENKINS_IP')
    JENKINS_PORT = config('JENKINS_PORT', default='JENKINS_PORT', cast=int)
    JENKINS_USER = config('JENKINS_USER', default='JENKINS_USER')
    JENKINS_PASW = config('JENKINS_PASW', default='JENKINS_PASW')
    c = Connection(JENKINS_IP, port=JENKINS_PORT, user=JENKINS_USER, connect_kwargs={'password': JENKINS_PASW})
    c.put(container_zip, remote=JENKINS_PATH)
    # # make call to jenkins to trigger build and shut down server
    res = requests.post(f'https://ide:113e1546e2c0046919b7434d8326adcc94@phil.codeln.com/job/copy_files_to_workspace/'
                        'buildWithParameters?directory_name={workspaceixzcyjq0hk9p3gtt}&candidate_name=juliet?token=1'
                        '13e1546e2c0046919b7434d8326adcc94')
    return HttpResponse('OK')
