import tkinter as widgets
from tkinter import messagebox, ttk

from funciones import agregar_al_carrito, buscar_productos, carrito_a_dataframe, quitar_del_carrito
from ventas import realizar_venta


def crear_aplicacion(inventario):
    carrito = []
    ventas = []

    ventana = widgets.Tk()
    ventana.title("Carrito de compra - Minimarket")
    ventana.geometry("950x680")

    widgets.Label(
        ventana,
        text="Carrito de compra - Minimarket",
        font=("Arial", 18, "bold"),
    ).pack(pady=(12, 2))
    widgets.Label(
        ventana,
        text="Selecciona productos, agrégalos al carrito y registra una venta.",
    ).pack(pady=(0, 10))

    marco_busqueda = widgets.LabelFrame(ventana, text="Buscar productos", padx=10, pady=10)
    marco_busqueda.pack(fill="x", padx=15, pady=5)

    widgets.Label(marco_busqueda, text="Producto:").grid(row=0, column=0, padx=5)
    entrada_busqueda = widgets.Entry(marco_busqueda, width=25)
    entrada_busqueda.grid(row=0, column=1, padx=5)

    widgets.Label(marco_busqueda, text="Categoría:").grid(row=0, column=2, padx=5)
    categoria = widgets.StringVar(value="Todas")
    lista_categorias = ttk.Combobox(
        marco_busqueda,
        textvariable=categoria,
        values=["Todas", "Abarrotes", "Bebidas", "Lácteos", "Limpieza"],
        state="readonly",
        width=15,
    )
    lista_categorias.grid(row=0, column=3, padx=5)

    tabla_productos = ttk.Treeview(
        marco_busqueda,
        columns=("codigo", "nombre", "categoria", "precio", "stock"),
        show="headings",
        height=7,
    )
    for columna, titulo, ancho in [
        ("codigo", "Código", 80),
        ("nombre", "Nombre", 220),
        ("categoria", "Categoría", 120),
        ("precio", "Precio", 100),
        ("stock", "Stock", 80),
    ]:
        tabla_productos.heading(columna, text=titulo)
        tabla_productos.column(columna, width=ancho)
    tabla_productos.grid(row=1, column=0, columnspan=5, pady=10)

    def cargar_productos():
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)

        resultados = buscar_productos(
            inventario,
            entrada_busqueda.get(),
            categoria.get(),
        )
        for _, producto in resultados.iterrows():
            tabla_productos.insert(
                "",
                "end",
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    producto["categoria"],
                    f"${int(producto['precio'])}",
                    int(producto["stock"]),
                ),
            )

    widgets.Button(marco_busqueda, text="Buscar", command=cargar_productos).grid(
        row=0, column=4, padx=5
    )

    marco_carrito = widgets.LabelFrame(ventana, text="Carrito de compra", padx=10, pady=10)
    marco_carrito.pack(fill="x", padx=15, pady=5)

    widgets.Label(marco_carrito, text="Cantidad:").grid(row=0, column=0, padx=5)
    entrada_cantidad = widgets.Spinbox(marco_carrito, from_=1, to=100, width=5)
    entrada_cantidad.grid(row=0, column=1, padx=5)

    tabla_carrito = ttk.Treeview(
        marco_carrito,
        columns=("codigo", "nombre", "precio", "cantidad", "subtotal"),
        show="headings",
        height=6,
    )
    for columna, titulo, ancho in [
        ("codigo", "Código", 80),
        ("nombre", "Nombre", 220),
        ("precio", "Precio", 100),
        ("cantidad", "Cantidad", 90),
        ("subtotal", "Subtotal", 110),
    ]:
        tabla_carrito.heading(columna, text=titulo)
        tabla_carrito.column(columna, width=ancho)
    tabla_carrito.grid(row=1, column=0, columnspan=6, pady=10)

    texto_total = widgets.StringVar(value="Total: $0")
    widgets.Label(
        marco_carrito,
        textvariable=texto_total,
        font=("Arial", 12, "bold"),
    ).grid(row=2, column=0, columnspan=6, sticky="e", pady=5)

    mensaje = widgets.StringVar(value="")
    widgets.Label(ventana, textvariable=mensaje, fg="darkgreen").pack(pady=5)

    salida = widgets.Text(ventana, height=9, width=110, state="disabled")
    salida.pack(padx=15, pady=5)

    def mostrar_texto(texto):
        salida.config(state="normal")
        salida.delete("1.0", widgets.END)
        salida.insert("1.0", texto)
        salida.config(state="disabled")

    def actualizar_carrito():
        for item in tabla_carrito.get_children():
            tabla_carrito.delete(item)

        tabla = carrito_a_dataframe(carrito)
        for _, item in tabla.iterrows():
            tabla_carrito.insert(
                "",
                "end",
                values=(
                    item["codigo"],
                    item["nombre"],
                    f"${int(item['precio'])}",
                    int(item["cantidad"]),
                    f"${int(item['subtotal'])}",
                ),
            )

        total = int(tabla["subtotal"].sum()) if not tabla.empty else 0
        texto_total.set(f"Total: ${total}")

    def agregar_producto():
        seleccion = tabla_productos.selection()
        if not seleccion:
            mensaje.set("Selecciona un producto de la tabla.")
            return

        codigo = tabla_productos.item(seleccion[0], "values")[0]
        try:
            cantidad = int(entrada_cantidad.get())
        except ValueError:
            mensaje.set("La cantidad debe ser un número entero.")
            return

        mensaje.set(agregar_al_carrito(inventario, carrito, codigo, cantidad))
        actualizar_carrito()

    def quitar_producto():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            mensaje.set("Selecciona un producto del carrito.")
            return

        codigo = tabla_carrito.item(seleccion[0], "values")[0]
        mensaje.set(quitar_del_carrito(carrito, codigo))
        actualizar_carrito()

    def vaciar_carrito():
        carrito.clear()
        mensaje.set("El carrito fue vaciado.")
        actualizar_carrito()

    def realizar_venta_interfaz():
        venta, texto = realizar_venta(inventario, carrito, ventas)
        mensaje.set(texto)
        if venta is None:
            return

        fecha = venta["fecha_hora"].strftime("%d/%m/%Y %H:%M")
        boleta = [
            f"BOLETA FICTICIA N° {venta['numero']}",
            f"Fecha y hora: {fecha}",
            "-" * 45,
        ]
        for item in venta["detalle"]:
            boleta.append(
                f"{item['nombre']} | {item['cantidad']} x "
                f"${item['precio']} = ${item['subtotal']}"
            )
        boleta.extend(["-" * 45, f"TOTAL: ${venta['total']}"])
        mostrar_texto("\n".join(boleta))
        actualizar_carrito()
        cargar_productos()
        messagebox.showinfo("Venta realizada", "La venta fue registrada correctamente.")

    widgets.Button(marco_carrito, text="Agregar al carrito", command=agregar_producto).grid(
        row=0, column=2, padx=5
    )
    widgets.Button(marco_carrito, text="Quitar producto", command=quitar_producto).grid(
        row=0, column=3, padx=5
    )
    widgets.Button(marco_carrito, text="Vaciar carrito", command=vaciar_carrito).grid(
        row=0, column=4, padx=5
    )
    widgets.Button(
        marco_carrito,
        text="Realizar venta",
        command=realizar_venta_interfaz,
    ).grid(row=0, column=5, padx=5)

    cargar_productos()
    ventana.mainloop()
