from django.contrib.auth import authenticate, alogin, login as authlogin, logout as authlogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Todo
from django.shortcuts import redirect


# Create your views here.

@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        text = request.POST.get('text').strip()
        print(text)
        if text:
            Todo.objects.create(text=text, user=request.user)
        return redirect('/')
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user).all()
        return render(request, 'todo/home.html', {'todos': todos})
    return render(request, 'todo/home.html')


def todo_delete(request, id):
    # todo = Todo.objects.get(id=id, user=request.user)
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect('/')


"""
 def todo_update(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        text = request.POST.get('text').strip()
        if text:
            todo.text = text
            todo.save()
            return redirect('/')
    else:
        return render(request, 'todo/base.html', {'todo': todo})
"""


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return redirect('todo:home')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid credentials'})
    return render(request, 'todo/login.html')


def logout(request):
    authlogout(request)
    return redirect('todo:login')

def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    print(username)
    if username and password and first_name and last_name and email:
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        return redirect('todo:login')

    return render(request, 'todo/signup.html')
