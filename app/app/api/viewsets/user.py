from rest_framework.response import Response
from app.serializers import input, output
from app.models.user import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils import timezone


class CreateUser(APIView):
    permission_classes = (AllowAny,)
    input_serializer_class = input.CreateUserInputSerializer
    output_serializer_class = output.UserOutputSerializer

    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            phone_number = input_serializer.validated_data.get('phone_number')
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'Phone number already registered.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(**input_serializer.validated_data)
            user.set_password(input_serializer.validated_data.get('password'))
            user.save()

            refresh = RefreshToken.for_user(user)
            output_serializer = self.output_serializer_class(user)
            return Response(
                {
                    'user': output_serializer.data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                },
                status=status.HTTP_201_CREATED
            )


class LoginUser(APIView):
    permission_classes = (AllowAny,)
    input_serializer_class = input.LoginUserInputSerializer
    output_serializer_class = output.UserOutputSerializer

    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        phone_number = input_serializer.validated_data['phone_number']
        password = input_serializer.validated_data['password']

        try:
            user = User.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(phone_number=phone_number, first_name="Unknown", last_name="")
            user.set_password(password)
            user.save()

        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        output_serializer = self.output_serializer_class(user)
        return Response(
            {
                'user': output_serializer.data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            },
            status=status.HTTP_200_OK
        )
