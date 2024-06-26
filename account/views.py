from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token= get_tokens_for_user(user)
            return Response({"token":token,"msg": "registration successfull"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                          

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            print(email)
            password=serializer.data.get('password')
            print(password)
            user = authenticate(email=email,password=password)
            print("user--",user)
            if user is not None:
                token= get_tokens_for_user(user)
                return Response({"token":token,"msg": "login successfull"}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email and password are not valid']}}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


