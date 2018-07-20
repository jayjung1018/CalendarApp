from django import forms
from pages.models import Task, Reminder

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'start', 'end']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Task Name"}),
            'start': forms.TimeInput(format="%H:%M", attrs={'size': '5', 'class':'timeinput', 'placeholder': "00:00 AM", 'pattern': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9] ([AaPp][Mm])'}),
            'end': forms.TimeInput(format="%H:%M", attrs={'size': '5', 'class':'timeinput', 'placeholder': "00:00 AM", 'pattern': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9] ([AaPp][Mm])'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data['start']
        end = cleaned_data['end']

        if (start > end):
            msg = "Start time must be less than end time!"
            raise forms.ValidationError("Start time must be less than End time")

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs=({'placeholder': "Reminder Name", 'class':'timeinput', 'size':'30'}))
        }
