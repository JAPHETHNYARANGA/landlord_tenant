from django.db import models 

class Chatbox(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} at {self.timestamp}: {self.message[:50]}"
