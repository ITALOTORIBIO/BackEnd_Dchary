from .models import Usuario, Producto, Dashboard
from .serializers import UsuarioSerializer, ProductoSerializer, DashboardSerializer, UserTokenSerializer
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView


from django.db.models import Sum
from .models import Producto, Dashboard

# def calcular_total_cantidad(request):
#     # Calcula la suma total de la columna "cantidad" en la tabla "Producto"
#     suma_cantidad = Producto.objects.aggregate(total=Sum('valor_total_ing_prod')).get('total')
    
#     # Crea una instancia de Dashboard y guarda la suma en la columna "total_cantidad"
#     resultado = Dashboard(total_valor_ingreso=suma_cantidad)
#     resultado.save()

#     # Redirecciona a otra vista o realiza cualquier acción adicional necesaria

#     # ...


##  APIS APIS APIS
class UsuarioViewset(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# class ProductoViewset(viewsets.ModelViewSet):
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer    

class Login(ObtainAuthToken):

    def post(self,request,*args,**kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso.'
                    }, status = status.HTTP_201_CREATED)
                else:
                    # all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    # if all_sessions.exists():
                    #     for session in all_sessions:
                    #         session_data = session.get_decoded()
                    #         if user.id == int(session_data.get('_auth_user_id')):
                    #             session.delete()
                    # token.delete()
                    # token = Token.objects.create(user = user)
                    # return Response({
                    #     'token': token.key,
                    #     'user': user_serializer.data,
                    #     'message': 'Inicio de Sesión Exitoso.'
                    # }, status = status.HTTP_201_CREATED)
                    token.delete()
                    return Response({
                        'error': 'Ya se ha iniciado sesión con este usuario.'
                    }, status = status.HTTP_409_CONFLICT)
            else:
                return Response({'error':'Este usuario no puede iniciar sesión.'}, 
                                    status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos.'},
                                    status = status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'Hola desde response'}, status = status.HTTP_200_OK)

class Logout(APIView):

    def get(self,request,*args,**kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()

            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminadas.'  
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message,'session_message':session_message},
                                    status = status.HTTP_200_OK)

            return Response({'error':'No se ha encontrado un usuario con estas credenciales.'},
                    status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se ha encontrado token en la petición.'}, 
                                    status = status.HTTP_409_CONFLICT)
        
    def post(self,request,*args,**kwargs):
        try:
            token = request.POST.get('token')
            token = Token.objects.filter(key = token).first()

            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminadas.'  
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message,'session_message':session_message},
                                    status = status.HTTP_200_OK)

            return Response({'error':'No se ha encontrado un usuario con estas credenciales.'},
                    status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se ha encontrado token en la petición.'}, 
                                    status = status.HTTP_409_CONFLICT)


## PRODUCTOS

class ProductoListApiView(ListAPIView):
    serializer_class = ProductoSerializer
    def get_queryset(self):
        return Producto.objects.all()    

class ProductoCreateApiView(CreateAPIView):
    serializer_class = ProductoSerializer

class ProductoDeleteView(DestroyAPIView):    
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()

class ProductoUpdateView(RetrieveUpdateAPIView):    
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()


## PRODUCTOS

class DashboardListApiView(APIView):
    def get(self, request):
        total_cantidad_ing = Producto.objects.aggregate(Sum('cant_ing_prod'))['cant_ing_prod__sum']
        total_cantidad_sal = Producto.objects.aggregate(Sum('cant_sal_prod'))['cant_sal_prod__sum']
        
        plata_ing = Producto.objects.aggregate(Sum('valor_total_ing_prod'))['valor_total_ing_prod__sum']
        plata_sal = Producto.objects.aggregate(Sum('valor_total_sal_prod'))['valor_total_sal_prod__sum']
        resultado, _ = Dashboard.objects.get_or_create(pk=1)  # Obtener o crear una instancia de Resultado

        resultado.total_valor_ingreso = plata_ing
        resultado.total_valor_salida = plata_sal
        
        resultado.total_cantidad_ingreso = total_cantidad_ing
        resultado.total_cantidad_salida = total_cantidad_sal
        resultado.save()
        return Response({'message': 'La suma de cantidad se ha calculado y guardado en total_cantidad.'})

    


        total_cantidad = Producto.objects.aggregate(Sum('cantidad'))['cantidad__sum']
        resultado, _ = Resultado.objects.get_or_create(pk=1)  # Obtener o crear una instancia de Resultado
        resultado.total_cantidad = total_cantidad
        resultado.save()
        return Response({'message': 'La suma de cantidad se ha calculado y guardado en total_cantidad.'})


