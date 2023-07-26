from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()

class Conversation(models.Model):
    questioner = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    response = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.prompt}: {self.response}"
