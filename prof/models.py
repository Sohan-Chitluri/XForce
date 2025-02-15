from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100,null=True, default="Using Star-Burst-Stream")
    name = models.CharField(max_length=100,null=True, blank=True)  # Name of the user
    age = models.PositiveIntegerField(null=True,blank=True)  # Age of the user
    def __str__(self):
        return self.user.username

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        overlapping_events = Schedule.objects.filter(
            user=self.user,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping_events.exists():
            raise ValidationError("This time slot overlaps with an existing schedule.")

    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"
