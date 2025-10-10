from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Utility function to create a notification record.
    
    Args:
        recipient (User): The user receiving the notification.
        actor (User): The user who performed the action.
        verb (str): A short description of the action (e.g. "liked your post").
        target (Model, optional): The object related to the notification (Post, Comment, etc.).
    """
    # Avoid sending notifications to self
    if recipient == actor:
        return None

    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ContentType.objects.get_for_model(target) if target else None,
        target_object_id=target.id if target else None,
    )
    return notification
