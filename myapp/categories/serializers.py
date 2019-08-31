from rest_framework import serializers

from categories.models import Category
from json import loads, dumps

# class RecursiveField(serializers.Serializer):

#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data





class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField('_get_children')
    parents = serializers.SerializerMethodField('_get_parents')
    siblings = serializers.SerializerMethodField('_get_siblings')

    def _get_siblings(self, obj):
        if obj.parents:
            serializer = SubCategorySerializer(obj.parents.children.all().exclude(id=obj.id), many=True)
        else:
            return []
        return serializer.data

    def _get_children(self, obj):
        serializer = SubCategorySerializer(obj.children, many=True)
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


    # def create(self, validated_data):
    #     print(validated_data)
    #     items_data = validated_data['children'][0]
    #     newlist = Category.objects.create(**validated_data)
    #     for item_data in items_data:
    #         Category.objects.create(parents=newlist, **item_data)
    #     return list
    #     # return Category.objects.create(**validated_data)


    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'children',
            'parents',
            'siblings'
            )




class SaveSerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True)
    # parents = RecursiveField(many=True, required=False)



    def create(self, validated_data):
        childrens = validated_data.pop('children', None)
        print(validated_data)
        # print(items_data)
        category = Category.objects.create(**validated_data)
        if childrens is not None:
            for children in childrens:
                # item = dict(item_data).pop('children', None)
                for item in [loads(dumps(children))]:
                    Category.objects.create(parents=category, **children)

                    self.create(validated_data=item)

            return category

        # return Category.objects.create(**validated_data)

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')
