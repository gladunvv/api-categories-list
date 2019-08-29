from rest_framework import serializers

from categories.models import Category


class ParentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class ChildCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)

class SiblingCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)



class CategorySerializer(serializers.ModelSerializer):


    children = serializers.SerializerMethodField('_get_children')
    parents = serializers.SerializerMethodField('_get_parents')
    siblings = serializers.SerializerMethodField('_get_siblings')


    def _get_siblings(self, obj):
        serializer = SiblingCategorySerializer(obj.parents.children.all().exclude(id=obj.id), many=True)
        return serializer.data

    def _get_children(self, obj):
        serializer = ChildCategorySerializer(obj.children, many=True)
        return serializer.data

    def _get_parents(self, obj):
        parent = Category.get.all()
        serializer = ParentCategorySerializer(parent, many=True)
        return serializer.data


    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'children',
            'parents',
            'siblings'
            )
