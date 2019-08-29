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
        # print('1 -------', obj.parents.children.all().exclude(id=obj.id))
        if obj.parents:
            serializer = SiblingCategorySerializer(obj.parents.children.all().exclude(id=obj.id), many=True)
        else:
            return []
        return serializer.data

    def _get_children(self, obj):
        print('2 --------', obj.children)
        serializer = ChildCategorySerializer(obj.children, many=True)
        return serializer.data

    def _get_parents(self, obj):
        parents_list = []
        if obj.parents:
            try:
                while obj.parents:
                    parents_list.append(obj.parents)
                    obj = obj.parents
            except:
                serializer = ParentCategorySerializer(parents_list, many=True)
                return serializer.data
        else:
            return []



    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'children',
            'parents',
            'siblings'
            )
