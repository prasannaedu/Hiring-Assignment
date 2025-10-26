# app/api/viewsets/scam.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.serializers import input, output
from app.models.scam import ScamRecord
from django.db import transaction


class CreateScamRecord(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    input_serializer_class = input.CreateScamRecordInputSerializer
    output_serializer_class = output.ScamRecordOutputSerializer

    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        with transaction.atomic():
            try:
                scam, created = ScamRecord.objects.get_or_create(
                    reported_by=user,
                    phone_number=input_serializer.validated_data['phone_number'],
                    defaults={
                        'description': input_serializer.validated_data.get('description', ''),
                        'created_by': user,
                        'updated_by': user
                    }
                )
                if not created:
                    return Response({'error': 'You have already reported this number.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                output_serializer = self.output_serializer_class(scam)
            except Exception as e:
                return Response({'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
