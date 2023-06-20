from django import views
from django.urls import path, include
from .views import UsuarioViewset, Login, Logout
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewset)

urlpatterns = [
    #VISTA PRINCIPAL
    path('',Login.as_view(), name = 'login'),
    path('api/', include(router.urls)),
    path('logout/', Logout.as_view(), name = 'logout'),
    #CLASIFICACION
    path('producto/listar',views.ProductoListApiView.as_view()),
    path('producto/actualizar',views.ProductoCreateApiView.as_view()),
    path('producto/eliminar/<pk>/',views.ProductoDeleteView.as_view()),
    path('producto/modificar/<pk>/',views.ProductoUpdateView.as_view()),
    #CLASIFICACION
    path('dashboard/listar',views.DashboardListApiView.as_view()),
    # path('dashboard/actualizar',views.DashboardCreateApiView.as_view()),
    # path('dashboard/eliminar/<pk>/',views.DashboardDeleteView.as_view()),
    # path('dashboard/modificar/<pk>/',views.DashboardUpdateView.as_view()),
  ]