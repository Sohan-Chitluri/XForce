from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from .models import Profile
from .forms import ProfileUpdateForm
from .models import Schedule
from .forms import ScheduleForm
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

def add_schedule(request):
    if request.method == "POST":
        title = request.POST["title"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]

        schedule = Schedule(
            user=request.user,  # Assign the logged-in user
            title=title,
            start_time=start_time,
            end_time=end_time,
        )

        try:
            schedule.save()  # Runs clean() before saving
            messages.success(request, "Schedule added successfully!")
            return redirect("schedule_list")
        except Exception as e:
            messages.error(request, str(e))  # Show validation errors

    return render(request, "add_schedule.html")
    
def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user).order_by('start_time')
    return render(request, "schedule_list.html", {"schedules": schedules})

def delete_schedule(request, schedule_id):  # Ensure request is passed
    schedule = get_object_or_404(Schedule, id=schedule_id, user=request.user)
    schedule.delete()
    return redirect('schedule_list')

def profile(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]

    # Simply render the profile page without handling profile picture upload
    return render(request, "prof/profile.html", {"profile": profile})


def home(request):
    return render(request, 'prof/home.html')  # Home Page

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")  # Redirect to home page after login
        else:
            return render(request, "prof/login.html", {"error": "Invalid credentials"})

    return render(request, "prof/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")  # Redirect to home page after logout

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login page after signup
    else:
        form = UserCreationForm()

    return render(request, "prof/register.html", {"form": form})

# This function is called after a Profile is saved
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# This function is called after a Profile is saved when updating
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

def update_profile(request):
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)  
            profile.user = request.user 
            profile.save()  
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'prof/update_profile.html', {'form': form})

