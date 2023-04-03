from django.db import models
from django.contrib.auth.models import User


class BudgetCategory(models.Model):
    category = models.CharField(max_length=128)
    def __str__(self):
        return self.category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    projected=models.PositiveIntegerField()
    actual=models.PositiveIntegerField()