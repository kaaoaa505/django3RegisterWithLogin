from django.contrib.auth import forms
from django.core.checks.messages import Error
from django.db.models.fields import DateTimeField
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from todo.forms import TodoForm
from .models import Todo


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': TodoForm()})
    else:
        try:
            formData = TodoForm(request.POST)
            newTodo = formData.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('dashboard')
        except ValueError:
            error = 'Invalid data value.'
            return render(request, 'todo/create.html', {'form': TodoForm(), 'error': error})


@login_required
def dashboard(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/dashboard.html', {'todos': todos})


@login_required
def completed(request):
    todos = Todo.objects.filter(
        user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed.html', {'todos': todos})


def home(request):
    return render(request, 'todo/home.html')


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = 'Invalid username or password.'
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': error})
        else:
            login(request, user)
            return redirect('dashboard')


@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def register(request):
    if request.method == 'GET':
        return render(request, 'todo/register.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                error = 'That username has already been taken, please choose a new username.'
                return render(request, 'todo/register.html', {'form': UserCreationForm(), 'error': error})
        else:
            error = 'Passwords did not match.'
            return render(request, 'todo/register.html', {'form': UserCreationForm(), 'error': error})


@login_required
def todoComplete(request, todo_pk):
    todoItem = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todoItem.dateCompleted = timezone.now()
        todoItem.save()
    return redirect('dashboard')


@login_required
def todoDelete(request, todo_pk):
    todoItem = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todoItem.delete()
    return redirect('dashboard')


@login_required
def todoView(request, todo_pk):
    error = ''
    todoItem = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todoItem)
    else:
        try:
            form = TodoForm(request.POST, instance=todoItem)
            form.save()
            return redirect('dashboard')
        except ValueError:
            error = 'Invalid data value.'
    return render(request, 'todo/todoView.html', {'todoItem': todoItem, 'form': form, 'error': error})
