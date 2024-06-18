from django.db import models

class Proovedor(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey("Marca", on_delete=models.SET_NULL, null=True, blank=True)




class Precio(models.Model):
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    proovedor = models.ForeignKey("Proovedor" , on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10 , decimal_places=2)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.producto} - {self.proovedor} : {self.precio}'

