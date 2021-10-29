"""TodoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # AuthApp
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),

    # TodosApp
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('completed/', views.completed, name='completed'),
    path('create/', views.create, name='create'),
    path('todo/<int:todo_pk>', views.todoView, name='todoView'),
    path('todo/<int:todo_pk>/complete', views.todoComplete, name='todoComplete'),
    path('todo/<int:todo_pk>/delete', views.todoDelete, name='todoDelete'),
]
