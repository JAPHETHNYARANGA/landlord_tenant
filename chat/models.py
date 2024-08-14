from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here

user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
message = models.TextField()
timestamp = models.DateTimeField(default=timezone.now)



def __str__(self):
    return  f"{self.user.username} at {self.timestamp}:{self:message[:50]}"