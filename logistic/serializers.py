from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=60)

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=200)
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        exclude = ['products']

    def validate_positions(self, value):
        if not value:
            raise serializers.ValidationError("the order items are not specified")
        items_ids = [item['product'].id for item in value]
        if len(items_ids) != len(set(items_ids)):
            raise serializers.ValidationError('duplicated items in the order')
        return value

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for item in positions:
            StockProduct.objects.create(stock=stock, **item)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for item in positions:
            product = item.pop('product')
            obj, created = StockProduct.objects.update_or_create(stock=stock, product=product, defaults=item)
        return stock
