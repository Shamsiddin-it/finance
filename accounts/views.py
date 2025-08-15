from rest_framework import status, permissions, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import *


class RegisterApiView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")
        email = request.data.get("email")
        
        if not username or not password1 or not password2 or not email:
            return Response("All the fields are required", status=status.HTTP_400_BAD_REQUEST)
        
        is_user = User.objects.filter(username=username).exists()
        if is_user:
            return Response("User already exists", status=status.HTTP_400_BAD_REQUEST)
        
        if password1 != password2:
            return Response("Passwords do not match", status=status.HTTP_400_BAD_REQUEST)
        
        if not "@" in email or not "." in email:
            return Response("Not a valid email", status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        return Response("User added successfully", status=status.HTTP_201_CREATED)
    

class LoginApiView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response("Both fields are required", status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] 
    def post(self, request):
        token = str(request.auth)
        user = request.user
        BlackListedToken.objects.create(user=user, token=token)
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)