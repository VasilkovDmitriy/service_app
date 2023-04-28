from django.db.models import F, Prefetch, Sum
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status

from clients.models import Client
from services.models import Subscription
from services.serializers import CreateSubscriptionSerializer, SubscriptionSerializer


class SubscriptionView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Subscription.objects.prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.select_related('user').only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price'))
        response.data = response_data

        return response

    @extend_schema(
        request=CreateSubscriptionSerializer,
        responses={201: CreateSubscriptionSerializer, 400: None},
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(
            {'id': instance.id}, status=status.HTTP_201_CREATED, headers=headers
        )
