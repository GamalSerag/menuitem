from rest_framework import serializers
from .models import MenuItemExtraItem, MenuItemExtra, MenuItemTypeItem, MenuItemType, MenuItem
from drf_writable_nested.serializers import WritableNestedModelSerializer



class MenuItemExtraItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemExtraItem
        fields = ['id', 'name', 'price']

class MenuItemExtraSerializer(WritableNestedModelSerializer):
    items = MenuItemExtraItemSerializer(many=True)

    class Meta:
        model = MenuItemExtra
        fields = ['id', 'title', 'items']

class MenuItemTypeItemSerializer(WritableNestedModelSerializer):
    class Meta:
        model = MenuItemTypeItem
        fields = ['id', 'name', 'price']

class MenuItemTypeSerializer(WritableNestedModelSerializer):
    items = MenuItemTypeItemSerializer(many=True)

    class Meta:
        model = MenuItemType
        fields = ['id', 'title', 'items']

class CustomJSONField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data

class MenuItemSerializer(WritableNestedModelSerializer):
    extras = MenuItemExtraSerializer(many=True)
    types = MenuItemTypeSerializer(many=True)
    sizes_and_prices = CustomJSONField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'image', 'ingredients', 'extras', 'types', 'sizes_and_prices']

    def create(self, validated_data):
        extras_data = validated_data.pop('extras', [])
        types_data = validated_data.pop('types', [])
        sizes_and_prices_data = validated_data.pop('sizes_and_prices', [])

        menu_item = MenuItem.objects.create(**validated_data)

        for extra_data in extras_data:
            items_data = extra_data.pop('items', [])
            extra = MenuItemExtra.objects.create(**extra_data)
            for item_data in items_data:
                MenuItemExtraItem.objects.create(extra=extra, **item_data)
            menu_item.extras.add(extra)  # Add the created extra to the menu item

        for type_data in types_data:
            items_data = type_data.pop('items', [])
            type_obj = MenuItemType.objects.create(**type_data)
            for item_data in items_data:
                MenuItemTypeItem.objects.create(type=type_obj, **item_data)
            menu_item.types.add(type_obj)  # Add the created type to the menu item

        menu_item.sizes_and_prices = sizes_and_prices_data
        menu_item.save()
        return menu_item