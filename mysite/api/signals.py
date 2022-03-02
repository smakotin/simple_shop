from api.tasks import send_mail_after_order
from cart.models import Order


def send_mail_after_order_signal(sender, **kwargs):
    send_mail_after_order('slamfromm@gmail.com')
