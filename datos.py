import pandas as pd


def crear_inventario():
    """Crea y devuelve el inventario inicial del minimarket."""
    datos = [
        {"codigo": "A001", "nombre": "Arroz 1 kg", "categoria": "Abarrotes", "precio": 1500, "stock": 20},
        {"codigo": "A002", "nombre": "Fideos 400 g", "categoria": "Abarrotes", "precio": 900, "stock": 35},
        {"codigo": "B001", "nombre": "Leche entera 1 L", "categoria": "Lácteos", "precio": 1200, "stock": 18},
        {"codigo": "B002", "nombre": "Yogur natural", "categoria": "Lácteos", "precio": 850, "stock": 25},
        {"codigo": "C001", "nombre": "Bebida cola 1.5 L", "categoria": "Bebidas", "precio": 1900, "stock": 12},
        {"codigo": "C002", "nombre": "Agua mineral 1.5 L", "categoria": "Bebidas", "precio": 1000, "stock": 30},
        {"codigo": "D001", "nombre": "Jabón líquido", "categoria": "Limpieza", "precio": 2500, "stock": 10},
        {"codigo": "D002", "nombre": "Esponja", "categoria": "Limpieza", "precio": 700, "stock": 40},
    ]
    return pd.DataFrame(datos)
