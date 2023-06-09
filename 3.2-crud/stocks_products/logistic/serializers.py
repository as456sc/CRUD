from logistic.models import Product,Stock,StockProduct
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields =['id','title','description']
        


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product','quantity','price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id','address','positions']
    # настройте сериализатор для склада
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for i in positions:
            new_stok_product = StockProduct.objects.create(product=i['product'], stock=stock, quantity=i['quantity'],price=i['price'])
            
        return stock

    




    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for i in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': i['quantity'], 'price': i['price']},product=i['product'], stock=stock)
        return stock