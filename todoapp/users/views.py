from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users import (
    serializers as user_serializers
)


class UserRegistrationAPIView(CreateAPIView):
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """
    permission_classes = [AllowAny]
    serializer_class = user_serializers.UserRegistrationSerializer


class UserLoginAPIView(CreateAPIView):
    """
        success response format
         {
           auth_token: ""
         }
    """
    permission_classes = [AllowAny]
    serializer_class = user_serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'auth_token': token.key}, status=status.HTTP_200_OK)
