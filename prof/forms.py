from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'start_time', 'end_time']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'age', 'bio']

