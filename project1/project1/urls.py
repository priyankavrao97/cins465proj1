"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from core import views as core_views
from tasks import views as task_views
from budget import views as budget_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home),
    path('tasks/', task_views.tasks),
    path('tasks/add/', task_views.add),
    path('tasks/edit/<int:id>/', task_views.edit),
    path('tasks/changeCompleted/<int:id>/', task_views.changeCompleted),
    path('budget/', budget_views.budget),
    path('budget/add/', budget_views.add),
    path('budget/edit/<int:id>/', budget_views.edit),
    path('about/', core_views.about),
    path('join/', core_views.join),
    path('login/', core_views.user_login),
    path('logout/', core_views.user_logout),
]
    
