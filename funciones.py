import pandas as pd


def buscar_productos(inventario, texto="", categoria="Todas"):
    resultados = inventario.copy()

    if texto:
        nombres = resultados["nombre"].str.lower()
        resultados = resultados[nombres.str.contains(texto.lower(), na=False)]

    if categoria != "Todas":
        resultados = resultados[resultados["categoria"] == categoria]

    return resultados


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    producto = inventario[inventario["codigo"] == codigo]

    if producto.empty:
        return "No se encontró el producto."

    if cantidad <= 0:
        return "La cantidad debe ser mayor que cero."

    producto = producto.iloc[0]
    cantidad_actual = 0

    for item in carrito:
        if item["codigo"] == codigo:
            cantidad_actual = item["cantidad"]
            break

    if cantidad_actual + cantidad > int(producto["stock"]):
        return "No hay suficiente stock disponible."

    if cantidad_actual > 0:
        for item in carrito:
            if item["codigo"] == codigo:
                item["cantidad"] += cantidad
                break
    else:
        carrito.append(
            {
                "codigo": producto["codigo"],
                "nombre": producto["nombre"],
                "precio": int(producto["precio"]),
                "cantidad": cantidad,
            }
        )

    return "Producto agregado al carrito."


def quitar_del_carrito(carrito, codigo):
    for item in carrito:
        if item["codigo"] == codigo:
            carrito.remove(item)
            return "Producto eliminado del carrito."

    return "El código no está en el carrito."


def calcular_total(carrito):
    return sum(item["precio"] * item["cantidad"] for item in carrito)


def carrito_a_dataframe(carrito):
    if not carrito:
        return pd.DataFrame(columns=["codigo", "nombre", "precio", "cantidad", "subtotal"])

    tabla = pd.DataFrame(carrito)
    tabla["subtotal"] = tabla["precio"] * tabla["cantidad"]
    return tabla[["codigo", "nombre", "precio", "cantidad", "subtotal"]]


def mostrar_carrito(carrito):
    if not carrito:
        return "<p>El carrito está vacío.</p>"

    tabla = carrito_a_dataframe(carrito)
    return tabla.to_html(index=False) + f"<h3>Total: ${calcular_total(carrito)}</h3>"

