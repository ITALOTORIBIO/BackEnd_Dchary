from rest_framework import serializers
from .models import User, Usuario, Producto, Dashboard
from django.db.models import Sum

class UsuarioSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Usuario
        fields= '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Producto
        fields= '__all__'

class DashboardSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Dashboard
        fields= '__all__'

    # def update(self, instance, validated_data):
    #     total_cantidad = Producto.objects.aggregate(Sum('valor_total_ing_prod'))['cantidad__sum']
    #     instance.total_valor_ingreso = total_cantidad
    #     instance.save()
    #     return instance    

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        updated_user = super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    def to_representation(self,instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }        