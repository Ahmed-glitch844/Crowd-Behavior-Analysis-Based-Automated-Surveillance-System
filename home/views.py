from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
import json
import os
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import execjs
import threading
# Create your views here.
from .prediction import Pred
from .live_classification import gen
from django.http import StreamingHttpResponse
import threading


def Del():
    fs = FileSystemStorage
    dir = r'C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\media'
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        fs.delete(name=file_path)
    file_path = None
    return


def register(request):
    return render(request, 'Register.html')


def login(request):
    return render(request, 'login.html')


def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        f_name = request.POST['F_name']
        L_name = request.POST['L_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validate user information
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('register')
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        # save the user information
        myuser = User.objects.create_user(
            username, email, password, first_name=f_name, last_name=L_name)
        # myuser.name = name
        # myuser.organization = organization
        # myuser.phone = phone
        myuser.save()
        messages.success(request, 'Registration is successful')
        return redirect('login')

    else:
        return HttpResponse('404 - not found.')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # messages.success(request, 'login is successful')
            return redirect('dashboard')
            # return render(request,'Dashboard.html',{'username':username})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return HttpResponse('404 - not found.')


@login_required()
def dashboard(request):
    return render(request, 'Dashboard.html', {'username': request.user.username})


def live_classification(request):
    return StreamingHttpResponse(
        gen(request.user.email), content_type="multipart/x-mixed-replace;boundary=frame")


@login_required()
def live(request):
    return render(request, 'live.html', {'username': request.user.username})


def send_json(request):
    with open(r"C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\logs.json", "r") as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)


@login_required()
def logs(request):
    return render(request, 'logs.html', {'username': request.user.username})


def Logout(request):
    with open(r'C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\var.js', 'r') as f:
        lines = f.readlines()

    # iterate over the lines and replace the value of myVariable
        for i, line in enumerate(lines):
            if "Value =" in line:
                lines[i] = "Value = 'Not Classified yet';\n"

    # write the modified lines back to the file
        with open(r'C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\var.js', 'w') as f:
            f.writelines(lines)
    logout(request)
    # Del()

    return redirect('login')


def load_video(request):
    f_path = request.FILES['Insert']
    store = FileSystemStorage()
    f_path = store.save(f_path.name, f_path)
    f_path = store.url(f_path)
    context = {'f_path': f_path, 'username': request.user.username}
    print(User.username)
    return render(request, 'Dashboard.html', context)


def Classify(request):
    with open(r'C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\var.js', 'r') as f:
        lines = f.readlines()

    # iterate over the lines and replace the value of myVariable
        for i, line in enumerate(lines):
            if "Value =" in line:
                lines[i] = "Value = 'Not Classified yet';\n"

    # write the modified lines back to the file
        with open(r'C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\var.js', 'w') as f:
            f.writelines(lines)
    f_name = ''
    if request.method == 'POST':
        f_name = str(request.FILES['Insert'])
        t2 = threading.Thread(target=Pred, args=[f_name])
        t2.start()
        return load_video(request)


def write_to_json(request):
    if request.method == 'POST':
        current_data = None
        data = json.loads(request.body)
        with open(r"C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\logs.json", "r") as f:
            if (os.stat(r"C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\logs.json").st_size != 0):
                current_data = json.load(f)

        with open(r"C:\Users\ahmed\Documents\python_projects\FYP_frontEnd\demo\static\css\logs.json", "w") as f:
            if current_data is None:
                l = [data]
                json.dump(l, f)
            else:
                current_data.append(data)
                json.dump(current_data, f)
        return JsonResponse("Successfully created", safe=False)


def assign_value(request):
    with open('C:/Users/ahmed/Documents/python_projects/FYP_frontEnd/demo/static/css/var.js', 'r') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    val = ctx.eval('Value')
    data = {'value': val}
    print("Val function")
    return JsonResponse(data, safe=False)
