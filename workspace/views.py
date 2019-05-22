from django.shortcuts import render
from decouple import config
# Create your views here.
def workspace(request):
    context = {
        'url': config('HOSTNAME')
    }
    return render(request,'workspace/workspace.html', context=context)
