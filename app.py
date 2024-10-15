from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1) # Habilita la redimensión de la ventana. (0,0) para deshabilitar.
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        #Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Candara', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=30) #Columnspan se indica cuantas columnas del grid va a utilizar

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0, padx=10, pady=5)

        #Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus() #Para que el cursor aparezca en este elemento
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0, padx=10, pady=5)

        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ")
        self.etiqueta_stock.grid(row=3, column=0, padx=10, pady=5)

        # Entry Stock
        self.stock = Entry(frame)
        self.stock.grid(row=3, column=1)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ")
        self.etiqueta_categoria.grid(row=4, column=0, padx=10, pady=5)

        # Entry Categoria
        self.categoria = Entry(frame)
        self.categoria.grid(row=4, column=1)

        # Botón Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Candara', 13, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=3, padx=10, pady=5, sticky=W+E) #Si no pongo STICKY, el botón sale centrado, al utilizarlo,
        # el botón se alarga hacia los extremos dejando el texto centrado. Sticky utiliza los puntos cardinales para hacer
        # referencia hacia dónde queremos expandir el objeto.

        #Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=5, columnspan=3, sticky=W+E)

        #Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Candara', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Candara', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#1', '#2', '#3'), style="mystyle.Treeview")
        self.tabla.grid(row=7, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='Stock', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('#3', text='Categoría', anchor=CENTER)  # Encabezado 2

        # Botones de editar y eliminar
        s = ttk.Style()
        s.configure('my.TButton', font=('Candara', 14, 'bold'))
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=7, column=0, sticky=W+E)
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto, style='my.TButton')
        boton_editar.grid(row=7, column=1, sticky=W+E)

        self.get_productos()

    #Función que conecta y consulta a la base de datos
    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        # Recorrer la tabla para limpiar la consulta
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        for fila in registros:
            print(fila) #Este print es de verificación en el terminal
            self.tabla.insert('', 0, text = fila[1], values = (fila[2], fila[3], fila[4]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0  # Me devuelve False o True

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0 # Me devuelve False o True

    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0 # Me devuelve False o True

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0 # Me devuelve False o True

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.stock.get(), self.categoria.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "Producto {} añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0, END) # Borrar el campo del principio al final
            self.precio.delete(0, END)
            self.stock.delete(0, END)
            self.categoria.delete(0, END)
            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and  self.validacion_stock() == False:
            print("El stock es obligatorio")
            self.mensaje["text"] = "Introduzca el stock existente para el producto, 0 para falta de existencias"
        elif self.validacion_nombre() and self.validacion_precio() and  self.validacion_stock() and self.validacion_categoria() == False:
            print("Introduzca una categoría para el producto")
            self.mensaje["text"] = "Introduzca una categoría para el producto"
        else:
            print("Todos los campos deben de ser rellenados")
            self.mensaje["text"] = "Revise que ha rellenado todos los campos"
        self.get_productos()

    def del_producto(self):
        #print(self.tabla.item(self.tabla.selection())) #Accedemos al elemento que esté seleccionado de la tabla
        #print(self.tabla.item(self.tabla.selection())["text"]) #Podemos acceder a su nombre
        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "El producto {} ha sido eliminado con éxito".format(nombre)
        self.get_productos()

    def edit_producto(self):
        print("Editar producto")
        self.mensaje["text"] = ""

        old_nombre = self.tabla.item(self.tabla.selection())["text"] #Creo la variable accediendo a nombre
        old_precio = self.tabla.item(self.tabla.selection())["values"][0] #Viene de un diccionario que nos crea, y accedemos a la posición 0
        old_stock = self.tabla.item(self.tabla.selection())["values"][1]
        old_categoria = self.tabla.item(self.tabla.selection())["values"][2]

        self. ventana_editar = Toplevel() #Crear una ventana nueva
        self.ventana_editar.title("Editar producto")
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Candara", 30, "bold"))
        titulo.grid(row=0, column=0)

        frame_ep =LabelFrame(self.ventana_editar, text="Editar el siguiente producto", font=('Candara', 15, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=25, padx=20)

        #Label nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=("Candara", 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0, padx=10, pady=5)
        #Entry nombre antiguo
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre), state="readonly", font=("Candara", 13))
        self.input_nombre_antiguo.grid(row=2, column=1, padx=10, pady=5)

        # Label nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Candara", 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0, padx=10, pady=5)
        # Entry nombre nuevo
        self.input_nombre_nuevo = Entry(frame_ep, font=("Candara", 13))
        self.input_nombre_nuevo.grid(row=3, column=1, padx=10, pady=5)

        #############

        # Label precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=("Candara", 13))
        self.etiqueta_precio_antiguo.grid(row=4, column=0, padx=10, pady=5)
        # Entry precio antiguo
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Candara", 13))
        self.input_precio_antiguo.grid(row=4, column=1, padx=10, pady=5)

        # Label precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Candara", 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0, padx=10, pady=5)
        # Entry precio nuevo
        self.input_precio_nuevo = Entry(frame_ep, font=("Candara", 13))
        self.input_precio_nuevo.grid(row=5, column=1, padx=10, pady=5)

        #############

        # Label stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=("Candara", 13))
        self.etiqueta_stock_antiguo.grid(row=6, column=0, padx=10, pady=5)
        # Entry stock antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                          state="readonly", font=("Candara", 13))
        self.input_stock_antiguo.grid(row=6, column=1, padx=10, pady=5)

        # Label stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=("Candara", 13))
        self.etiqueta_stock_nuevo.grid(row=7, column=0, padx=10, pady=5)
        # Entry stock nuevo
        self.input_stock_nuevo = Entry(frame_ep, font=("Candara", 13))
        self.input_stock_nuevo.grid(row=7, column=1, padx=10, pady=5)

        #############

        # Label categoria antigua
        self.etiqueta_categoria_antiguo = Label(frame_ep, text="Categoría antigua: ", font=("Candara", 13))
        self.etiqueta_categoria_antiguo.grid(row=8, column=0, padx=10, pady=5)
        # Entry categoria antiguo
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                         state="readonly", font=("Candara", 13))
        self.input_categoria_antiguo.grid(row=8, column=1, padx=10, pady=5)

        # Label categoria nuevo
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoría nueva: ", font=("Candara", 13))
        self.etiqueta_categoria_nuevo.grid(row=9, column=0, padx=10, pady=5)
        # Entry categoria nuevo
        self.input_categoria_nuevo = Entry(frame_ep, font=("Candara", 13))
        self.input_categoria_nuevo.grid(row=9, column=1, padx=10, pady=5)

        s = ttk.Style()
        s.configure('my.TButton', font=('Candara', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                                self.input_nombre_antiguo.get(),
                                                                                                self.input_precio_nuevo.get(),
                                                                                                self.input_precio_antiguo.get(),
                                                                                                self.input_stock_nuevo.get(),
                                                                                                self.input_stock_antiguo.get(),
                                                                                                self.input_categoria_nuevo.get(),
                                                                                                self.input_categoria_antiguo.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W+E, padx=10, pady=5)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nuevo_stock, antiguo_stock, nuevo_categoria, antiguo_categoria):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, stock = ?, categoria = ? WHERE nombre = ? AND precio = ? AND stock = ? AND categoria = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nuevo_stock != '' and nuevo_categoria != '':
            # Si el usuario escribe nuevo nombre, nuevo precio, nuevo stock y nueva categoría, se cambian todos
            parametros = (nuevo_nombre, nuevo_precio, nuevo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_stock != '' and nuevo_categoria == '':
            # Si el usuario escribe nuevo nombre, nuevo precio, nuevo stock se cambian y mantiene categoría
            parametros = (nuevo_nombre, nuevo_precio, nuevo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_stock == '' and nuevo_categoria != '':
            # Si el usuario escribe nuevo nombre, nuevo precio, nueva categoría se cambian y mantiene stock
            parametros = (nuevo_nombre, nuevo_precio, antiguo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nuevo_stock == '' and nuevo_categoria == '':
            # Si el usuario escribe nuevo nombre, nuevo precio se cambian y mantiene stock y categoría
            parametros = (nuevo_nombre, nuevo_precio, antiguo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_stock != '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (nuevo_nombre, antiguo_precio, nuevo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_stock == '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo precio y el nuevo stock, se mantiene el precio y el stock anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_stock != '' and nuevo_categoria == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior y categoria anterior
            parametros = (nuevo_nombre, antiguo_precio, nuevo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nuevo_stock == '' and nuevo_categoria == '':
            # Si el usuario deja vacio el nuevo precio y el nuevo stock, se mantiene el precio y el stock anterior  y categoria anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_stock != '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nuevo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_stock == '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo nombre y el nuevo stock, se mantiene el nombre y el stock anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_stock != '' and nuevo_categoria == '':
            # Si el usuario deja vacio el nuevo nombre y la nueva categoria, se mantiene el nombre anterior y la categoría anterior
            parametros = (antiguo_nombre, nuevo_precio, nuevo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nuevo_stock == '' and nuevo_categoria == '':
            # Si el usuario deja vacio el nuevo nombre, la nueva categoría y el nuevo stock, se mantiene el nombre la categoría y el stock anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_stock != '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo nombre y el nuevo precio, se mantiene el nombre y el precio
            parametros = (antiguo_nombre, antiguo_precio, nuevo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_stock == '' and nuevo_categoria != '':
            # Si el usuario deja vacio el nuevo nombre, el nuevo precio y el nuevo stock, se mantiene el nombre, el precio y el stock
            parametros = (antiguo_nombre, antiguo_precio, antiguo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nuevo_stock != '' and nuevo_categoria == '':
            # Si el usuario deja vacio el nuevo nombre, el nuevo precio y el nuevo categoria, se mantiene el nombre, el precio y la categoria
            parametros = (antiguo_nombre, antiguo_precio, nuevo_stock, antiguo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            producto_modificado = True
        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario

if __name__== "__main__":
    root = Tk()
    app = Producto(root)
    root.mainloop() #Con esto conseguimos que la ventana se mantenga a la espera