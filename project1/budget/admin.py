from django.contrib import admin

# Register your models here.
from budget.models import Budget,BudgetCategory

#Register your models here
admin.site.register(Budget)
admin.site.register(BudgetCategory)
