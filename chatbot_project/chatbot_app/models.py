from django.db import models
from django.utils import timezone

class QACache(models.Model):
    question_id = models.CharField(max_length=255, unique=True, default="string")
    question = models.TextField(unique=True)
    answer = models.TextField(unique=True)
    created_time = models.DateTimeField()
    
    def __str__(self):
        return self.answer
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_time = timezone.now() 
        return super(QACache, self).save(*args, **kwargs)