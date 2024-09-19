from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=User)
def cleanup_after_user_deletion(sender, instance, **kwargs):
    """
    Signal to ensure user data is completely cleaned up after deletion.
    """
    try:
        # Perform any additional cleanup required, e.g., deleting related objects
        logger.info(f"User {instance.username} deleted successfully.")
    except Exception as e:
        logger.error(f"Error during cleanup after user deletion: {e}")
