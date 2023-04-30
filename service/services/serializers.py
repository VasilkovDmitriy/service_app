from rest_framework import serializers

from services.models import Client, Plan, Service, Subscription


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    service = ServiceSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    class Meta:
        model = Subscription
        fields = ('id', 'plan', 'service', 'client_name', 'email', 'price')


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), write_only=True)
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), write_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'client', 'service', 'plan')
