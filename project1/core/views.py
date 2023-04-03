from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.forms import LoginForm, JoinForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from tasks.models import TaskCategory, Task
from budget.models import BudgetCategory, Budget
import json

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    completed = Task.objects.filter(user=request.user, is_completed=True).count()
    pending = Task.objects.filter(user=request.user, is_completed=False).count()
    taskspie=[completed, pending]
    print(taskspie)

    projvalues = list(Budget.objects.filter(user=request.user).values_list('projected', flat=True))
    print(projvalues)
    actvalues = list(Budget.objects.filter(user=request.user).values_list('actual', flat=True))
    print(actvalues)
    context={
        'taskspie':json.dumps(taskspie),
        'projvalues':json.dumps(projvalues),
        'actvalues':json.dumps(actvalues)
    }
    return render(request, 'core/core.html',context)


def about(request):
    return render(request, 'core/about.html')

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'core/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'core/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'core/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'core/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")