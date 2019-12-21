from django.db import models
from django.contrib.auth.models import User

class UserAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    drowsiness_count = models.IntegerField()

    def __str__(self):
        return str(self.user.username)+' : '+str(self.start_time)
