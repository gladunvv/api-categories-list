from rest_framework import serializers

from categories.models import Category
from json import loads, dumps


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField('_get_children')
    parents = serializers.SerializerMethodField('_get_parents')
    siblings = serializers.SerializerMethodField('_get_siblings')

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'children',
            'parents',
            'siblings'
        )

    def _get_siblings(self, obj):
        if obj.parents:
            serializer = SubCategorySerializer(obj.parents.children.all().exclude(id=obj.id), many=True)
            print(serializer.data)
        else:
            return []
        return serializer.data

    def _get_children(self, obj):
        serializer = SubCategorySerializer(obj.children, many=True)
        print(serializer.data)
        return serializer.data

    def _get_parents(self, obj):
        parents_list = []

        if obj.parents is not None:
            while obj.parents:
                parents_list.append(obj.parents)
                obj = obj.parents
            serializer = SubCategorySerializer(parents_list, many=True)
            return serializer.data

        else:
            return parents_list


class SaveCategorySerializer(serializers.ModelSerializer):

    children = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')


    def create(self, validated_data):

        children_data = validated_data.pop('children')
        category = Category.objects.create(**validated_data)
        for children in children_data:
            Category.objects.create(parents=category, **children)
        return category
