from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField("Date created", blank=True)
    updated = models.DateTimeField("Date updated", blank=True, null=True)

    def __str__(self):
        '''Object representation'''
        return self.title
    
    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        if not self._state.adding:
            self.updated = timezone.now()
        else:
            if not self.title:
                self.title = "untitled"
            self.created = timezone.now()
        return super(Note, self).save(*args, **kwargs)
