from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from app.models.user import User
from app.models.contact import Contact
from app.models.scam import ScamRecord
from app.serializers.output import search as output

def get_query_type(query):
    """Determine if the query is phone number or name."""
    if not query:
        return None
    return 'phone_number' if query[0].isdigit() else 'name'

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    output_serializer_class = output.SearchOutputSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'Search query is required.'}, status=status.HTTP_400_BAD_REQUEST)

        search_type = get_query_type(query)
        results = []

        if search_type == 'phone_number':
            results = list(User.objects.filter(phone_number__startswith=query)) + \
                      list(Contact.objects.filter(phone_number__startswith=query))
        else:
            results = list(User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))) + \
                      list(Contact.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)))

        serialized = self.output_serializer_class(results, many=True).data
        unique_results = list({item['phone_number']: item for item in serialized}.values())

        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(unique_results, request)
        return paginator.get_paginated_response(paginated_results)

class SearchDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    output_user_serializer_class = output.SearchDetailsUserOutputSerializer
    output_contact_serializer_class = output.ContactOutputSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = self.output_user_serializer_class(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            pass

        try:
            contact = Contact.objects.get(id=id)
            serializer = self.output_contact_serializer_class(contact)
            return Response(serializer.data)
        except Contact.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
