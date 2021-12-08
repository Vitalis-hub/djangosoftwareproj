from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager
from django.contrib.auth.decorators import login_required

def mylogin(request):
    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt, password=ptxt)
            print(user)
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt, password=ptxt)
            if user != None:
                login(request, user)
                return redirect('/panel')

    return render(request, 'front/signin.html')

def panel(request):
    if not request.user.is_authenticated:
        return redirect('/mylogin')
    return render(request, 'back/panel.html')

def register(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Input Your Name"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if password1 != password2:
            msg = "Your Password Didn't Match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0

        for i in password1:
            if i > '0' and i < '9':
                count1 = 1
            if i > 'A' and i < 'z':
                count2 = 1
            if i > 'a' and i < 'z':
                count3 = 1
            if i > '!' and i < '(':
               count4 = 1

        if count1 == 0 or count2 == 0 or count3 == 0 or  count4 == 0:
            msg = "Your Password id Not Strong"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(password1) < 8:
            msg = "Your Password Must Be Atleast 8 Characters"
            return render(request, 'front/msgbox.html', {'msg': msg})

        #if the current password does not exist in the database. The password isn't a previous one
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:
            
            ip, is_routable = get_client_ip(request)

            if ip is None:
                ip = '0.0.0.0'

            try:
                response = DbIpCity.get(ip, api_key = 'free')
                country = response.country + ' | ' + response.city
            except:
                country = 'unknown'

            user = User.objects.create_user(username=uname, email=email, password=password1)
            b = Manager(name = name, utxt = uname, email=email, ip=ip, country=country)
            b.save()

    return render(request, 'front/signin.html')
