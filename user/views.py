from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from .serializers import UserSerializer

### Registration
class Registration(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

### Login
class Login(APIView):

    throttle_classes = [UserRateThrottle]

    def post(self, request):
        user = authenticate(
            username = request.data.get("username"), password=request.data.get("password")
        )
        # 이미 회원가입 되 유저의 경우
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

### Logout
