from django.shortcuts import render
from .models import User
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework import response, status


class UserRegisterAPIView(GenericAPIView):
    """ View accessible by anyone to register into the SoftDeskAPI """

    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,
                                            status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)