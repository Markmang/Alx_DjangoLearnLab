from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import User  # ✅ Direct import from your custom user model


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target or ''}"

