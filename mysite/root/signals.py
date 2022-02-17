from django.contrib.auth.models import Group
from cart.models import Cart


def add_group_for_user_signal(sender, instance, created, **kwargs):
    """Add a user to the client group and create a shopping cart for the created user"""

    if created:
        group = Group.objects.get(name='client')
        cart = Cart(user=instance)
        cart.save()
        instance.groups.add(group)