from django.shortcuts import render, redirect
from django.views import generic
from .forms import TaskForm, ReminderForm
from .models import Task, Reminder
from django.urls import reverse_lazy
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'pages/home.html'
    redirect_field_name = 'pages/home.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #form stuff
        form = TaskForm()
        context['form'] = form

        #get tasks from database
        tasks = Task.objects.filter(user=self.request.user).order_by('start')
        context['tasks'] = tasks

        #get reminders from database
        reminderForm = ReminderForm()
        context['reminderForm'] = reminderForm

        reminders = Reminder.objects.filter(user=self.request.user)
        context['reminders'] = reminders

        return context

    def post(self, request, *args, **kwargs):
        if ('name' in request.POST):
            form = ReminderForm(request.POST)
        else:
            form = TaskForm(request.POST)


        if (form.is_valid()):
            newObject = form.save(commit=False)
            newObject.user = request.user
            newObject.save()

            return render(request, self.template_name, self.get_context_data())
        else:
            context = self.get_context_data()
            if ('name' in form):
                context['reminderForm'] = form
            else:
                context['form'] = form #need the form with the raised errors
        return render(request, self.template_name, context)

def deleteTaskView(request, pk):
    task = Task.objects.get(pk=pk)
    Task.delete(task)

    return redirect(reverse_lazy('pages:home'))

def getEvents(request):
    tasks = Task.objects.filter(user=request.user).order_by('start').values('title', 'start', 'end')
    data = list(tasks)
    return JsonResponse(data, safe=False)

def removeReminder(request, pk):
    reminder = Reminder.objects.get(pk=pk)
    Reminder.delete(reminder)

    return redirect(reverse_lazy('pages:home'))

def resetViews(request):
    user = request.user
    tasks = Task.objects.filter(user=request.user)
    tasks.delete()

    return redirect(reverse_lazy('pages:home'))
