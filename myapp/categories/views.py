from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryView(APIView):

    def get(self, request, pk):

        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
