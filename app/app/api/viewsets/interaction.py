from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import get_object_or_404

from app.models.interaction import Interaction
from app.models.contact import Contact
from app.serializers.input.interaction import InteractionSerializer, SpamReportCreateSerializer
from app.serializers.output.interaction import InteractionOutputSerializer


# ✅ Standard pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ✅ Create Interaction (call/message/spam)
class CreateInteractionView(generics.CreateAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()  # The serializer already assigns `initiator`


# ✅ Recent Interactions (with optional filtering)
class RecentInteractionsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    serializer_class = InteractionOutputSerializer

    def get(self, request):
        interaction_type = request.query_params.get('type')
        interactions = Interaction.objects.filter(initiator=request.user)

        if interaction_type:
            interactions = interactions.filter(type=interaction_type.lower())

        interactions = interactions.order_by('-timestamp')
        paginator = self.pagination_class()
        paginated = paginator.paginate_queryset(interactions, request)
        serializer = self.serializer_class(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)


# ✅ Top Contacts — most frequent receivers (users + contacts)
class TopContactsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        top_users = (
            Interaction.objects.filter(initiator=request.user, receiver_user__isnull=False)
            .values(
                'receiver_user__id',
                'receiver_user__first_name',
                'receiver_user__last_name',
                'receiver_user__phone_number'
            )
            .annotate(interaction_count=Count('id'))
            .order_by('-interaction_count')[:10]
        )

        top_contacts = (
            Interaction.objects.filter(initiator=request.user, receiver_contact__isnull=False)
            .values(
                'receiver_contact__id',
                'receiver_contact__first_name',
                'receiver_contact__last_name',
                'receiver_contact__phone_number'
            )
            .annotate(interaction_count=Count('id'))
            .order_by('-interaction_count')[:10]
        )

        return Response({
            'top_users': list(top_users),
            'top_contacts': list(top_contacts)
        }, status=status.HTTP_200_OK)


# ✅ Spam Reports (GET for aggregated reports, POST for creating new)
class SpamReportsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardResultsSetPagination
    serializer_class = InteractionOutputSerializer

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        spam_interactions = Interaction.objects.filter(type='spam')

        if start_date:
            spam_interactions = spam_interactions.filter(timestamp__gte=start_date)
        if end_date:
            spam_interactions = spam_interactions.filter(timestamp__lte=end_date)

        aggregated = (
            spam_interactions.values(
                'receiver_user__phone_number',
                'receiver_contact__phone_number'
            )
            .annotate(report_count=Count('id'))
            .order_by('-report_count')
        )

        paginator = self.pagination_class()
        paginated = paginator.paginate_queryset(list(aggregated), request)
        return paginator.get_paginated_response(paginated)

    def post(self, request):
        serializer = SpamReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_id = serializer.validated_data['contact_id']

        contact = get_object_or_404(Contact, id=contact_id)
        user = request.user

        spam_interaction = Interaction.objects.create(
            initiator=user,
            receiver_contact=contact,
            type='spam',
            timestamp=timezone.now(),
            metadata={}
        )

        return Response({
            'id': spam_interaction.id,
            'receiver_contact': str(contact.id),
            'type': spam_interaction.type,
            'timestamp': spam_interaction.timestamp
        }, status=status.HTTP_201_CREATED)
