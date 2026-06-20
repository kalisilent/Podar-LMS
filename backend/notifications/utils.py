from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(recipient, title, message, notif_type="general", link=""):
    """Create notification and push via WebSocket."""
    notif = Notification.objects.create(
        recipient=recipient, title=title, message=message,
        notif_type=notif_type, link=link)
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{recipient.id}",
            {"type": "send_notification", "data": {
                "id": str(notif.id), "title": title, "message": message,
                "notif_type": notif_type, "link": link,
            }})
    except Exception:
        pass  # WebSocket not available
    return notif
