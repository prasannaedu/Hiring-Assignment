from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.serializers.input.contact import CreateContactInputSerializer
from app.serializers.output import ContactOutputSerializer
from app.models.contact import Contact
from django.db import transaction

class CreateContact(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    input_serializer_class = CreateContactInputSerializer
    output_serializer_class = ContactOutputSerializer

    def post(self, request):
        serializer = self.input_serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user

        with transaction.atomic():
            contact, created = Contact.objects.get_or_create(
                created_by=user,
                phone_number=serializer.validated_data['phone_number'],
                defaults={
                    'first_name': serializer.validated_data['first_name'],
                    'last_name': serializer.validated_data.get('last_name', ''),
                    'updated_by': user
                }
            )
            if not created:
                return Response({'error': 'Contact with this phone number already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)

            output_serializer = self.output_serializer_class(contact)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
