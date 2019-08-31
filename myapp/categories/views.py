from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from categories.models import Category
from categories.serializers import CategorySerializer, SaveSerializer


class CategoryView(APIView):

    def get(self, request, pk):

        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryPostView(APIView):
    
    def post(self, request):
            category = request.data
            print(category)
            serializer = SaveSerializer(data=category)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
