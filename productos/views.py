from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto, Precio, Proovedor, Marca
from decimal import Decimal, InvalidOperation
from .forms import SubirArchivos_fenix, SubirArchivos_palomar, SubirArchivos_electrimat

import pandas as pd
from django.utils.timezone import now
import datetime


def lista_de_productos(request):
    return render(request, 'eleccion_lista.html')




def manejo_archivos_fenix(file):
    try:
        proveedor_nombre = 'Distribuidora Sanitaria Fenix'
        proveedor, _ = Proovedor.objects.get_or_create(nombre=proveedor_nombre)
        Precio.objects.filter(proovedor=proveedor).delete()
        Producto.objects.filter(precio__proovedor=proveedor).delete()

        df = pd.read_excel(file, skiprows=8)

        print("Columnas del archivo Excel:", df.columns.tolist())
        print("Primeras filas del DataFrame:\n", df.head())

        columnas_esperadas = ['CODIGO', 'DESCRIPCION', 'U/M', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9']
        columnas_archivo = df.columns.tolist()

        if not all(col in columnas_archivo for col in columnas_esperadas):
            raise ValueError("El archivo Excel no tiene las columnas esperadas.")

        df = df.rename(columns={'DESCRIPCION': 'descripcion', 'Unnamed: 9': 'precio'})
        df = df[['descripcion', 'precio']]

        for index, row in df.iterrows():
            if pd.isnull(row['descripcion']):
                continue

            try:
                precio = str(row['precio']).replace(',', '').replace('$', '').strip()
                precio_decimal = Decimal(precio)
                precio_entero = int(precio_decimal)
                precio_final = Decimal(precio_entero).quantize(Decimal('1'))
            except (InvalidOperation, ValueError):
                raise ValueError(f"El valor de precio '{row['precio']}' no es un número decimal válido.")

            producto, _ = Producto.objects.get_or_create(nombre=row['descripcion'])
            Precio.objects.update_or_create(
                producto=producto,
                proovedor=proveedor,
                defaults={'precio': precio_final}
            )
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo Excel: {e}")

def listar_y_subir_productos_fenix(request):
    if request.method == 'POST':
        form = SubirArchivos_fenix(request.POST, request.FILES)
        if form.is_valid():
            manejo_archivos_fenix(request.FILES['file'])
    else:
        form = SubirArchivos_fenix()

    productos = Producto.objects.filter(precio__proovedor__nombre='Distribuidora Sanitaria Fenix')
    precios = Precio.objects.filter(proovedor__nombre='Distribuidora Sanitaria Fenix')
    return render(request, 'listar_productos_fenix.html', {'form': form, 'productos': productos, 'precios': precios})

def manejo_archivos_palomar(file):
    try:
        proveedor_nombre = 'Distrito Palomar'
        proveedor, _ = Proovedor.objects.get_or_create(nombre=proveedor_nombre)
        Precio.objects.filter(proovedor=proveedor).delete()
        Producto.objects.filter(precio__proovedor=proveedor).delete()

        df = pd.read_excel(file, skiprows=8)

        print("Columnas del archivo Excel:", df.columns.tolist())
        print("Primeras filas del DataFrame:\n", df.head())

        columnas_esperadas = ['Unnamed: 0', 'Marca', 'Codigo', 'Descripcion', 'Caja', 'Precio', 'Pre. + IVA']
        columnas_archivo = df.columns.tolist()

        if not all(col in columnas_archivo for col in columnas_esperadas):
            raise ValueError("El archivo Excel no tiene las columnas esperadas.")

        df = df.rename(columns={'Marca': 'marca', 'Descripcion': 'descripcion', 'Pre. + IVA': 'precio'})
        df = df[['descripcion', 'precio', 'marca']]

        for index, row in df.iterrows():
            if pd.isnull(row['descripcion']):
                continue

            try:
                precio = str(row['precio']).replace(',', '').replace('$', '').strip()
                precio_decimal = Decimal(precio)
                precio_entero = int(precio_decimal)
                precio_final = Decimal(precio_entero).quantize(Decimal('1'))
            except (InvalidOperation, ValueError):
                raise ValueError(f"El valor de precio '{row['precio']}' no es un número decimal válido.")

            producto, _ = Producto.objects.get_or_create(nombre=row['descripcion'])
            marca, _ = Marca.objects.get_or_create(nombre=row['marca'])

            if not producto.marca:
                producto.marca = marca
                producto.save()

            Precio.objects.update_or_create(
                producto=producto,
                proovedor=proveedor,
                defaults={'precio': precio_final}
            )
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo Excel: {e}")

def listar_y_subir_productos_palomar(request):
    if request.method == 'POST':
        form = SubirArchivos_palomar(request.POST, request.FILES)
        if form.is_valid():
            manejo_archivos_palomar(request.FILES['file'])
    else:
        form = SubirArchivos_palomar()

    productos = Producto.objects.filter(precio__proovedor__nombre='Distrito Palomar')
    precios = Precio.objects.filter(proovedor__nombre='Distrito Palomar')
    return render(request, 'listar_productos_palomar.html', {'form': form, 'productos': productos, 'precios': precios})

def manejo_archivos_electrimat(file):
    try:
        proveedor_nombre = 'Electrimat'
        proveedor, _ = Proovedor.objects.get_or_create(nombre=proveedor_nombre)
        Precio.objects.filter(proovedor=proveedor).delete()
        Producto.objects.filter(precio__proovedor=proveedor).delete()

        df = pd.read_excel(file, skiprows=7)

        print("Columnas del archivo Excel:", df.columns.tolist())
        print("Primeras filas del DataFrame:\n", df.head())

        columnas_esperadas = ['### VARIOS ###', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6' , 'Unnamed: 7', 'Unnamed: 8']
        columnas_archivo = df.columns.tolist()

        if not all(col in columnas_archivo for col in columnas_esperadas):
            raise ValueError("El archivo Excel no tiene las columnas esperadas.")

        df = df.rename(columns={ 'Unnamed: 1': 'descripcion', 'Unnamed: 2': 'precio'})
        df = df[['descripcion', 'precio']]

        for index, row in df.iterrows():
            if pd.isnull(row['descripcion']):
                continue

            try:
                precio = str(row['precio']).replace(',', '').replace('$', '').strip()
                precio_decimal = Decimal(precio)
                precio_entero = int(precio_decimal)
                precio_final = Decimal(precio_entero).quantize(Decimal('1'))
            except (InvalidOperation, ValueError):
                raise ValueError(f"El valor de precio '{row['precio']}' no es un número decimal válido.")

            producto, _ = Producto.objects.get_or_create(nombre=row['descripcion'])

            Precio.objects.update_or_create(
                producto=producto,
                proovedor=proveedor,
                defaults={'precio': precio_final}
            )
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo Excel: {e}")

def listar_y_subir_productos_electrimat(request):
    if request.method == 'POST':
        form = SubirArchivos_electrimat(request.POST, request.FILES)
        if form.is_valid():
            manejo_archivos_electrimat(request.FILES['file'])
    else:
        form = SubirArchivos_electrimat()

    productos = Producto.objects.filter(precio__proovedor__nombre='Electrimat')
    precios = Precio.objects.filter(proovedor__nombre='Electrimat')
    return render(request, 'listar_productos_electrimat.html', {'form': form, 'productos': productos, 'precios': precios})
