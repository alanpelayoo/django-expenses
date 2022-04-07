
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.contrib import messages
from expenses.forms import ExpenseForm
from .models import Project,Category,Expense
from django.views.generic import CreateView
from .forms import ExpenseForm
import json

def projects_list(request):
    project_ev = Project.objects.exists()
    project_list = Project.objects.all()
    if request.method == 'DELETE':
        id = json.loads(request.body)['id']
        project = get_object_or_404(Project, id=id)
        project.delete()
        print("borrado")
        return HttpResponse('')
    return render(request,'expenses/project_list.html',{'project_list':project_list,'project_ev':project_ev})

def project_detail(request,project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == 'GET':
        category_list = Category.objects.all()
        expense_ev = project.expenses.exists()
        return render(request,'expenses/project_detail.html',{'project':project, 'expense_list':project.expenses.all(),'expense_ev':expense_ev,'category_list':category_list} )
    elif request.method == 'POST':
        #process the form
        form = ExpenseForm(request.POST) #populate the expenseform with the request POST
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category'] 
            category = get_object_or_404(Category,name=category_name)
            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()
            messages.success(request, f"Movimiento agregado: {title}")
        else:
            for msg in form.errors.as_data():
                messages.error(request, f"{msg}: {form.errors[msg].as_data()}")
                
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        return HttpResponse('')
    return HttpResponseRedirect(project_slug)
    
class ProjectCreateView(CreateView):
    model = Project
    template_name = 'expenses/add-project.html'
    fields = ('name','autor')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request,f"Projecto agrecado agregado: {self.request.POST['name']}")
        return HttpResponseRedirect('/' + self.get_success_url())
    def get_success_url(self):
        return slugify(self.request.POST['name'])

