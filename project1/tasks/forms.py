from django import forms
from django.contrib.auth.models import User
from tasks.models import Task, TaskCategory

class TaskEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    category = forms.ModelChoiceField(queryset=TaskCategory.objects.all())
    class Meta():
        model = Task
        fields = ('description', 'category')