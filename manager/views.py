from django.shortcuts import render, get_object_or_404, redirect
from .models import Manager
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def manager_group(request):
    
    # login check start
    # if not request.user.is_authenticated:
    #     #return redirect('mylogin')
    #     pass
    #login check end

    return render(request, 'back/manager_group.html')
