from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.models import TaskCategory, Task
from tasks.forms import TaskEntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def tasks(request):
	if(TaskCategory.objects.count() == 0):
		TaskCategory(category = "Home").save()
		TaskCategory(category = "School").save()
		TaskCategory(category = "Work").save()
		TaskCategory(category = "Self Improvement").save()		
		TaskCategory(category = "Other").save()

	if (request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		Task.objects.filter(id=id).delete()
		return redirect("/tasks/")
	else:
		table_data = Task.objects.filter(user=request.user)
		context = {
                    "table_data": table_data
		}
		return render(request, 'tasks/tasks.html', context)

@login_required(login_url='/login/')
def add(request):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = TaskEntryForm(request.POST, files=request.FILES)
			if (add_form.is_valid()):
				taskEntry = add_form.save(commit=False)
				taskEntry.user = request.user
				taskEntry.save()
				return redirect("/tasks/")
			else:
				context = {
                    "form_data": add_form
				}
				return render(request, 'tasks/add.html', context)
		else:
			# Cancel
			return redirect("/tasks/")
	else:
		context = {
            "form_data": TaskEntryForm()
		}
	return render(request, 'tasks/add.html', context)

@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		# Load Journal Entry Form with current model data.
		taskEntry = Task.objects.get(id=id)
		form = TaskEntryForm(instance=taskEntry)
		context = {"form_data": form}
		return render(request, 'tasks/edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = TaskEntryForm(request.POST)
			if (form.is_valid()):
				taskEntry = form.save(commit=False)
				taskEntry.user = request.user
				taskEntry.id = id
				taskEntry.save()
				return redirect("/tasks/")
			else:
				context = {
                    "form_data": form
				}
				return render(request, 'tasks/add.html', context)
		else:
			#Cancel
			return redirect("/tasks/") 
			
@login_required(login_url='/login/')
def changeCompleted(request, id):
	if (request.method == "GET"):
		taskEntry = Task.objects.get(id=id)

		if taskEntry.is_completed:
			taskEntry.is_completed = False
		else:
			taskEntry.is_completed = True
		
		taskEntry.save()
		return redirect("/tasks/")