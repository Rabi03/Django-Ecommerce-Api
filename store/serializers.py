from dataclasses import field
from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem,Product,Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','unit_price','price_with_tax','collection']

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product):
        return product.unit_price*Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description','date']
    
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)


class BasicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']
    
    total_price=serializers.SerializerMethodField(method_name='calculate_total_price')
    product=BasicProductSerializer()

    def calculate_total_price(self,item):
        return item.quantity*item.product.unit_price
        

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    class Meta:
        model=Cart
        fields=['id','total_price','items']
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self,cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No Product with the given ID is not found")
        return value


    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id =serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product=BasicProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','unit_price','quantity']


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']    
