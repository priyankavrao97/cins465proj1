from django.shortcuts import render, redirect
from django.http import HttpResponse
from budget.models import BudgetCategory, Budget
from budget.forms import BudgetEntryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.

@login_required(login_url='/login/')
def budget(request):
    if(BudgetCategory.objects.count() == 0):
        BudgetCategory(category = "Food").save()
        BudgetCategory(category = "Clothing").save()
        BudgetCategory(category = "Housing").save()
        BudgetCategory(category = "Education").save()
        BudgetCategory(category = "Entertainment").save()
        BudgetCategory(category = "Other").save()
        

    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Budget.objects.filter(id=id).delete()
        return redirect("/budget/")
    else:
        print("budget else")
        table_data = Budget.objects.filter(user=request.user)
        context = {
                    "table_data": table_data
        }
        prosum=Budget.objects.filter(user=request.user).aggregate(Sum('projected'))['projected__sum']
        print(prosum)
        actsum=Budget.objects.filter(user=request.user).aggregate(Sum('actual'))['actual__sum']
        print(actsum)
        if prosum and actsum:
            diff=prosum-actsum
            budget
            if(diff>0):
                budgetType='surplus'
            else:
                budgetType='deficit'
            diff=abs(diff)
            context['budgetType']=budgetType
            context['diff']=diff

        return render(request, 'budget/budget.html', context)

@login_required(login_url='/login/')
def add(request):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = BudgetEntryForm(request.POST, files=request.FILES)
			if (add_form.is_valid()):
				budgetEntry = add_form.save(commit=False)
				budgetEntry.user = request.user
				budgetEntry.save()
				return redirect("/budget/")
			else:
				context = {
                    "form_data": add_form
				}
				return render(request, 'budget/add.html', context)
		else:
			# Cancel
			return redirect("/budget/")
	else:
		context = {
            "form_data": BudgetEntryForm()
		}
	return render(request, 'budget/add.html', context)

@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		# Load Journal Entry Form with current model data.
		budgetEntry = Budget.objects.get(id=id)
		form = BudgetEntryForm(instance=budgetEntry)
		context = {"form_data": form}
		return render(request, 'budget/edit.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = BudgetEntryForm(request.POST)
			if (form.is_valid()):
				budgetEntry = form.save(commit=False)
				budgetEntry.user = request.user
				budgetEntry.id = id
				budgetEntry.save()
				return redirect("/budget/")
			else:
				context = {
                    "form_data": form
				}
				return render(request, 'budget/add.html', context)
		else:
			#Cancel
			return redirect("/budget/")
