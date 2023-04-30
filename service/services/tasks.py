from datetime import datetime
import time
from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
from django.db import transaction


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().filter(
            id=subscription_id
        ).annotate(
            annotate_price=F('service__full_price') - F('service__full_price') * F('plan__discount_percent') / 100
        ).first()

        subscription.price = subscription.annotate_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)

        subscription.comment = str(datetime.now())
        subscription.save()
