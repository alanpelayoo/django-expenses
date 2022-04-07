

from django.db import models
from django.utils.text import slugify
class Project(models.Model):
    name = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100,unique=True,blank=True)
    pagado = 0
    no_pagado = 0
    total = 0

    def save(self,*args, **kwargs): #Generate slug auto when we hit save
        self.slug = slugify(self.name)
        super(Project,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def paid(self):
        expense_list = Expense.objects.filter(project=self)
        total_paid = 0

        for expensee in expense_list:
            if expensee.category.name == "Abono":
                total_paid+=expensee.amount
        self.pagado=total_paid
        return total_paid
    def unpaid(self):
        expense_list = Expense.objects.filter(project=self)
        total_unpaid = 0
        for expensee in expense_list:
            if expensee.category.name == "Gasto":
                total_unpaid+=expensee.amount
        self.no_pagado=total_unpaid
        return total_unpaid

    def total(self):
        total = self.pagado-self.no_pagado
        return total

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



# def save(self,*args, **kwargs): #Generate slug auto when we hit save
#         self.slug = slugify(self.name)
#         super(Project,self).save(*args, **kwargs)
    
#     def __str__(self):
#         return self.name
    
#     def paid(self):
#         expense_list = Expense.objects.filter(project=self)
#         total_paid = 0

#         for expensee in expense_list:
#             if expensee.category.name == "Abono":
#                 total_paid+=expensee.amount
#         return total_paid
#     def unpaid(self):
#         expense_list = Expense.objects.filter(project=self)
#         total_unpaid = 0
#         for expensee in expense_list:
#             if expensee.category.name == "Gasto":
#                 total_unpaid+=expensee.amount
#         return total_unpaid

#     def total(self):
#         expense_list = Expense.objects.filter(project=self)
#         total_unpaid = 0
#         total_paid = 0
#         for expensee in expense_list:
#             if expensee.category.name == "Gasto":
#                 total_unpaid+=expensee.amount
#             elif expensee.category.name == "Abono":
#                 total_paid+=expensee.amount
#         return total_paid-total_unpaid

#quitar pagado no pagod y toal