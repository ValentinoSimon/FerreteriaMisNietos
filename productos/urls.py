from django.contrib import admin
from django.urls import path
from django.urls import include, path
from .views import   listar_y_subir_productos_fenix , listar_y_subir_productos_palomar , listar_y_subir_productos_electrimat , lista_de_productos

urlpatterns = [
    path('', lista_de_productos, name='lista_de_productos'),
    path('lista/fenix', listar_y_subir_productos_fenix, name='listar_productos_fenix'),
    path('lista/palomar', listar_y_subir_productos_palomar, name='listar_productos_palomar'),
    path('lista/electrimat', listar_y_subir_productos_electrimat, name='listar_productos_electrimat'),

]