from django.shortcuts import render
from employee.models import User, LogNoteBook
from storage.models import Location
from django.template import loader
from django.http import HttpResponse  
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from employee.forms import UserForm
from allauth.socialaccount.models import SocialAccount
from datetime import date

class authView():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_login'] = True
        if self.request.user.is_authenticated:  
            context['username'] = self.request.user.username
            if SocialAccount.objects.filter(user=self.request.user).exists():
                context['extra_data'] = SocialAccount.objects.get(user=self.request.user).extra_data
        return context 

def index(request):
    template = loader.get_template('index.html')
    context = {}  
    context['show_login'] = True
    if request.user.is_authenticated:  
        context['username'] = request.user.username 
    return HttpResponse(template.render(context, request))

class UserEdit(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_edit.html'
    slug_field = 'username'
    success_url = reverse_lazy('employee:index')

class EmployeeList(authView, ListView):
    model = User
    context_object_name = "employees"
    template_name = "employees.html"
    def get_queryset(self):
        queryset = User.objects.filter(groups__name='teacher').all()
        return queryset

def get_notebook(request, card, loc=1):
    if User.objects.filter(id_card=card).exists():
        current_user = User.objects.filter(id_card=card).first()
        current_location = Location.objects.filter(id=loc).first()
        log = LogNoteBook.objects.create(location=current_location, employee=current_user)
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
class LogNoteBookList(authView, ListView):
    model = LogNoteBook
    context_object_name = "lognotebook"
    template_name = "lognotebook.html"