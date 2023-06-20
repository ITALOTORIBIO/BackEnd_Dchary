from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=40)
    rol = models.CharField(max_length=20)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=15)
         
    def __str__(self):
        return self.username

    class Meta:
        verbose_name='Worker'
        verbose_name_plural='Workers'    

    
class Producto(models.Model):
    
    nom_prod = models.CharField(max_length=200, primary_key=True)
    precio_prod = models.DecimalField(default=0,max_digits=10, decimal_places=2) 
    unidad_prod = models.CharField(max_length=200)    
    cant_min_prod = models.DecimalField(default=0,max_digits=6, decimal_places=1)   
    estado_prod = models.CharField(editable=False)

    cant_prod = models.DecimalField(default=0,max_digits=6, decimal_places=1)   
    cant_ing_prod = models.DecimalField(default=0,max_digits=6, decimal_places=1)   
    cant_sal_prod = models.DecimalField(default=0,max_digits=6, decimal_places=1)   

    valor_total_prod = models.DecimalField(default=0,max_digits=10, decimal_places=2,editable=False)
    valor_total_ing_prod = models.DecimalField(default=0,max_digits=10, decimal_places=2,editable=False)
    valor_total_sal_prod = models.DecimalField(default=0,max_digits=10, decimal_places=2,editable=False)


    def save(self, *args, **kwargs):

        self.cant_prod = self.cant_ing_prod-self.cant_sal_prod

        self.valor_total_ing_prod = self.cant_ing_prod*self.precio_prod
        self.valor_total_sal_prod = self.cant_sal_prod*self.precio_prod

        self.valor_total_prod = self.valor_total_ing_prod-self.valor_total_sal_prod

        if self.cant_prod>self.cant_min_prod :
            self.estado_prod = "Ok"        
        elif self.cant_prod == self.cant_min_prod :
            self.estado_prod = "Warning"
        else:
            self.estado_prod = "Danger"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom_prod

    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering = ['nom_prod']     


class Dashboard(models.Model):
    total_valor_ingreso = models.DecimalField(default=0,max_digits=10, decimal_places=2) 
    total_valor_salida = models.DecimalField(default=0,max_digits=10, decimal_places=2) 
    
    total_cantidad_ingreso = models.DecimalField(default=0,max_digits=10, decimal_places=2) 
    total_cantidad_salida = models.DecimalField(default=0,max_digits=10, decimal_places=2) 

    # def calcular_suma_y_guardar(self, *args, **kwargs):
    #     suma_total = Producto.objects.aggregate(Sum('valor_total_ing_prod'))['cantidad__sum']
    #     self.total_valor_ingreso = suma_total
    #     super().save(*args, **kwargs)        

    def __str__(self):
        return self.total_valor_ingreso

    class Meta:
        verbose_name='tablero'
        verbose_name_plural='tableros'     

# @receiver(post_save, sender=Producto)
# def calcular_suma_y_guardar(sender, instance, created, **kwargs):
#     if created:
#         suma_total = Producto.objects.aggregate(models.Sum('valor_total_ing_prod'))['cantidad__sum']
#         Dashboard.objects.create(total_valor_ingreso=suma_total)
#     else:
#         suma_total = Producto.objects.aggregate(models.Sum('valor_total_ing_prod'))['cantidad__sum']
#         Dashboard.objects.update(total_valor_ingreso=suma_total)           
    
class UserManager(BaseUserManager):
    def _create_user(self, username, email, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True)
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'