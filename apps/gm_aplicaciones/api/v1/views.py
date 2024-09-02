from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from ...models import Aplicacion
from .serializers import AplicacionSerializer
from ...authentication import CustomJWTAuthentication


class AuthenticacionAPIView(APIView):
    permission_classes = [AllowAny]  # Permitimos cualquier acceso inicialmente
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        auth_result = self.authentication_classes[0]().authenticate(request)
        if auth_result is None:
            return Response({"detail": "Token inválido o no proporcionado."}, status=status.HTTP_401_UNAUTHORIZED)
        print(f"auth_result {auth_result}")
        user, token = auth_result
        return Response({
            "detail": "Token válido.",
            "user_id": user.id,
            "token": str(token)
        }, status=status.HTTP_200_OK)

    
class ApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def get(self, request, id=None):
        if id:
            user = get_object_or_404(Aplicacion, id=id)
            serializer = AplicacionSerializer(user)
            return Response(serializer.data)
        else:
            users = Aplicacion.objects.all()
            serializer = AplicacionSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AplicacionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        user = get_object_or_404(Aplicacion, id=id)
        serializer = AplicacionSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        user = get_object_or_404(Aplicacion, id=id)
        serializer = AplicacionSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)