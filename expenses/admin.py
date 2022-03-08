from django.contrib import admin
from .models import Project,Category,Expense

admin.site.register(Project)
admin.site.register(Expense)
admin.site.register(Category)