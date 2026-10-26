from datetime import datetime


def realizar_venta(inventario, carrito, ventas):
    """Registra una venta y descuenta las cantidades del inventario."""
    if not carrito:
        return None, "El carrito está vacío."

    for item in carrito:
        filas = inventario[inventario["codigo"] == item["codigo"]]

        if filas.empty:
            return None, f"No se encontró el producto {item['codigo']}."

        stock_actual = int(filas.iloc[0]["stock"])
        if item["cantidad"] > stock_actual:
            return None, (
                f"Stock insuficiente para {item['nombre']}. "
                f"Disponible: {stock_actual}."
            )

    detalle = []
    total = 0

    for item in carrito:
        subtotal = item["precio"] * item["cantidad"]
        detalle.append(
            {
                "codigo": item["codigo"],
                "nombre": item["nombre"],
                "precio": item["precio"],
                "cantidad": item["cantidad"],
                "subtotal": subtotal,
            }
        )
        total += subtotal

    for item in carrito:
        filtro = inventario["codigo"] == item["codigo"]
        inventario.loc[filtro, "stock"] -= item["cantidad"]

    venta = {
        "numero": len(ventas) + 1,
        "fecha_hora": datetime.now(),
        "detalle": detalle,
        "total": total,
    }

    ventas.append(venta)
    carrito.clear()
    return venta, "Venta realizada correctamente."


def mostrar_boleta(venta):
    fecha = venta["fecha_hora"].strftime("%d/%m/%Y %H:%M")
    html = f"<h2>Boleta ficticia N° {venta['numero']}</h2>"
    html += f"<p><b>Fecha y hora:</b> {fecha}</p>"
    html += "<table><tr><th>Producto</th><th>Cantidad</th>"
    html += "<th>Precio</th><th>Subtotal</th></tr>"

    for item in venta["detalle"]:
        html += (
            f"<tr><td>{item['nombre']}</td>"
            f"<td>{item['cantidad']}</td>"
            f"<td>${item['precio']}</td>"
            f"<td>${item['subtotal']}</td></tr>"
        )

    html += "</table>"
    html += f"<h3>Total: ${venta['total']}</h3>"
    return html


def exportar_venta_txt(venta, ruta):
    """Guarda una boleta simple en formato TXT."""
    fecha = venta["fecha_hora"].strftime("%d/%m/%Y %H:%M")

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(f"BOLETA FICTICIA N° {venta['numero']}\n")
        archivo.write(f"Fecha y hora: {fecha}\n")
        archivo.write("-" * 45 + "\n")

        for item in venta["detalle"]:
            archivo.write(
                f"{item['nombre']} | {item['cantidad']} x "
                f"${item['precio']} = ${item['subtotal']}\n"
            )

        archivo.write("-" * 45 + "\n")
        archivo.write(f"TOTAL: ${venta['total']}\n")
