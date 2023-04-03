from django import forms
from django.contrib.auth.models import User
from budget.models import Budget, BudgetCategory

class BudgetEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    category = forms.ModelChoiceField(queryset=BudgetCategory.objects.all())
    class Meta():
        model = Budget
        fields = ('description', 'category','projected','actual')