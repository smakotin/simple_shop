from datetime import timedelta
from api.tasks import send_mail_after_order
from cart.models import Order


def send_mail_after_order_signal(sender, **kwargs):
    notification_minutes = kwargs['instance'].notification.minutes
    execution_date = kwargs['instance'].execution_date
    notification_date = execution_date - timedelta(minutes=notification_minutes)
    send_mail_after_order.apply_async(('slamfromm@gmail.com',), eta=notification_date)
