from api.tasks import send_mail_after_order
from cart.models import Order


def send_mail_after_order_signal(sender, **kwargs):
    notification_minutes = kwargs['instance'].notification.minutes
    send_mail_after_order.apply_async(('slamfromm@gmail.com',), countdown=notification_minutes * 60)
