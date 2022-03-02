from time import sleep

from celery import shared_task


@shared_task
def add_cel(n):
    sleep(n)
    print('hellooooooooo')
