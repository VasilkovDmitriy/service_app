from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import set_comment, set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'Service ({self.name}, {self.full_price})'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)


class Plan(models.Model):
    PLAN_TYPES = (
        ("full", "Full"),
        ("student", "Student"),
        ("discount", "Discount"),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self) -> str:
        return f'Plan ({self.plan_type}, {self.discount_percent})'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name="subscriptions", on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name="subscriptions", on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name="subscriptions", on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('client', 'service', 'plan'), name='unique_subscription'
            ),
        )

    def __str__(self) -> str:
        return f'Subscription ({self.id})'
    
    def save(self, *args, **kwargs):
        is_created = self.pk is None
        super().save(*args, **kwargs)

        if is_created:
            set_price.delay(self.id)
            set_comment.delay(self.id)
