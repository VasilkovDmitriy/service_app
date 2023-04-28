from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

from services.models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    class Meta:
        model = Subscription
        fields = ('id', 'plan', 'client_name', 'email', 'price')


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    client = serializers.IntegerField(write_only=True)
    service = serializers.IntegerField(write_only=True)
    plan = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'client', 'service', 'plan')
