from tkinter import *
from tkinter import messagebox, ttk
import pymysql
from fpdf import FPDF

def menu_pantalla(): 
    global pantalla
    pantalla = Tk()
    pantalla.geometry("400x250")
    pantalla.title("Bienvenido")
    pantalla.iconbitmap("icono.ico")

    Label(text="Empresa Tecnológica Mic20", bg="darkmagenta", fg="white", width="300", height="3", font=("sans serif", 15)).pack()
    Label(text="").pack()

    Button(text="Iniciar Sesión", height="3", width="30", command=inicia_sesion).pack()
    Label(text="").pack()

    Button(text="Registrar", height="3", width="30", command= registrar ).pack()

    pantalla.mainloop()

def inicia_sesion():
    global pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.geometry("400x300")
    pantalla1.title("Inicio de Sesión")
    pantalla1.iconbitmap("icono.ico")

    Label(pantalla1, text="Inicio de Sesión", bg="darkmagenta", fg="white", width="300", height="3", font=("sans serif", 15)).pack()
    Label(pantalla1, text="").pack()

    global nombre_usuario_verify
    global contrasena_verify

    nombre_usuario_verify = StringVar()
    contrasena_verify = StringVar()

    global nombre_usuario_entry
    global contrasena_entry

    Label(pantalla1, text="Usuario").pack()
    nombre_usuario_entry = Entry(pantalla1, textvariable=nombre_usuario_verify)
    nombre_usuario_entry.pack()
    nombre_usuario_entry.focus()
    Label(pantalla1).pack()

    Label(pantalla1, text="Contraseña").pack()
    contrasena_entry = Entry(pantalla1, show="*", textvariable=contrasena_verify)
    contrasena_entry.pack()
    Label(pantalla1).pack()
    Button(pantalla1, text="Mostrar contraseña", command=toggle_password_visibility).pack()

    Button(pantalla1, text="Iniciar Sesión", command=validacion_datos).pack()

def registrar(): 
    global pantalla2
    pantalla2 = Toplevel(pantalla)
    pantalla2.geometry("400x300")
    pantalla2.title("Registro")
    pantalla2.iconbitmap("icono.ico")

    global nombre_usuario_entry
    global contrasena_entry
    
    nombre_usuario_entry=StringVar()
    contrasena_entry=StringVar()

    Label (pantalla2, text="Datos de registro" , bg="darkmagenta", fg="white", width="300", height="3", font=("sans serif", 15)).pack()
    Label (pantalla2, text="").pack()

    Label (pantalla2, text="Usuario").pack()
    nombre_usuario_entry= Entry(pantalla2)
    nombre_usuario_entry.pack()
    Label (pantalla2).pack()

    Label (pantalla2, text="Contraseña").pack()
    contrasena_entry= Entry(pantalla2, show="*")
    contrasena_entry.pack()
    Label (pantalla2).pack()
    Button(pantalla2, text="Mostrar contraseña", command=toggle_password_visibility).pack()

    Button(pantalla2, text="Registrar", command=inserta_datos).pack()

def inserta_datos():

    bd = pymysql.connect(
        host = "localhost",
        user="root",
        passwd="",
        db="bd"
    )

    if len(contrasena_entry.get()) <= 8:
        caracter = any(CHAR in ".,*+%$" for CHAR in contrasena_entry.get())

        if caracter:

            fcursor=bd.cursor()

            sql="INSERT INTO login (usuario, contrasena) VALUES ('{0}', '{1}')".format(nombre_usuario_entry.get(), contrasena_entry.get())

            try:
                fcursor.execute(sql)
                bd.commit()
                messagebox.showinfo(message="Registro Exitoso", title="Aviso")
            except:
                bd.rollback()
                messagebox.showinfo(message="No registrado", title="Aviso")

            bd.close()

        else: 
            messagebox.showinfo(title="Caracteres", message="La contraseña debe contener al menos uno de los siguientes carácteres especiales .,*+%$")

    else: 
        messagebox.showinfo(title="Caracteres", message="La contraseña puede contener hasta 8 caracteres")

def validacion_datos():
    bd = pymysql.connect(
        host = "localhost",
        user="root",
        passwd="",
        db="bd"
    )

    if len(contrasena_entry.get()) <= 8:
        caracter = any(CHAR in ".,*+%$" for CHAR in contrasena_entry.get())

        if caracter:

            fcursor=bd.cursor()

            sql="SELECT * FROM login WHERE usuario='"+nombre_usuario_entry.get()+"' and contrasena='"+contrasena_entry.get()+"'"

            fcursor.execute(sql)

            resultado= fcursor.fetchall()

            if resultado:
                listar_datos()
            else:
                messagebox.showinfo(title="Usuario no registrado", message="Usuario y contraseña incorrecta")

            bd.close()

        else: 
            messagebox.showinfo(title="Caracteres", message="La contraseña debe contener al menos uno de los siguientes carácteres especiales .,*+%$")

    else: 
        messagebox.showinfo(title="Caracteres", message="La contraseña puede contener hasta 8 caracteres")

def listar_datos():
    global pantalla3
    pantalla3 = Toplevel(pantalla1)
    pantalla3.geometry("750x600")
    pantalla3.title("Facturación")
    pantalla3.iconbitmap("icono.ico")

    boton1 = Button(pantalla3, text="Registrar producto", command= registrar_p)
    boton1.grid(row=0,column=0)
    boton2= Button(pantalla3, text="Facturas realizadas", command= factura)
    boton2.grid(row=0,column=1)

    c1 = Label (pantalla3, text="Datos del cliente", fg="black", height="3", font=("sans serif", 15))
    c1.grid(row=2,column=0, columnspan=2)

    c2 = Label (pantalla3, text="RIF")
    c2.grid(row=4,column=0)
    rif= Entry(pantalla3)
    rif.grid(row=4,column=1)

    c3 = Label (pantalla3, text="Nombre")
    c3.grid(row=4,column=2)
    nom_c= Entry(pantalla3)
    nom_c.grid(row=4,column=3)

    c4 = Label (pantalla3, text="Datos de los Productos", fg="black", height="3", font=("sans serif", 15))
    c4.grid(row=5,column=0, columnspan=2)

    c5 = Label (pantalla3, text="Producto")
    c5.grid(row=6,column=0)
    
    tp = list()
    lista = listar_prod()
    option_var = StringVar(pantalla3)

    if lista:
        for p in lista:
            tp.append(p)

        option_menu = ttk.OptionMenu(
            pantalla3,
            option_var,
            tp[0],
            *tp)
        option_menu.grid(row=6,column=1)
        option_menu.config(width=20)
    else: 
        c_np = Label (pantalla3, text="No hay productos registrados")
        c_np.grid(row=6,column=1)

    c6 = Label (pantalla3, text="Cantidad")
    c6.grid(row=7,column=0)
    cant= Entry(pantalla3)
    cant.grid(row=7,column=1)

    c7 = Label (pantalla3, text="Descuento")
    c7.grid(row=8,column=0)
    descuento= Entry(pantalla3)
    descuento.grid(row=8,column=1)

    def agg():
        if lista: 
            tabla_prod.insert('',0,text=cant.get(),
                    values=(option_var.get(), descuento.get()))
        else: 
            messagebox.showinfo(title="Aviso", message="Debe seleccionar un producto")

    boton_agg = Button(pantalla3, text="Agregar", command= agg)
    boton_agg.grid(row=8,column=2)

    c = Label (pantalla3, text="")
    c.grid(row=9,column=0)

    tabla_prod = ttk.Treeview(pantalla3, 
    column = ('Producto', 'Precio'))
    tabla_prod.grid(row=10,column=1, columnspan= 7)

    tabla_prod.column('#0', anchor = S)
    tabla_prod.heading('#0', text='Cantidad')
    tabla_prod.column('#1', anchor = S)
    tabla_prod.heading('#1', text='Producto')
    tabla_prod.column('#2', anchor = S)
    tabla_prod.heading('#2', text='Descuento')

    c = Label (pantalla3, text="")
    c.grid(row=17,column=0)

    def generar_factura():
        bd = pymysql.connect(
            host = "localhost",
            user="root",
            passwd="",
            db="bd"
        )
        
        fcursor=bd.cursor()

        if len(rif.get()) != 0 and len(nom_c.get()) != 0:
            if len(tabla_prod.get_children()) > 0:

                sql="INSERT INTO cliente (rif,n_cliente) VALUES ('{0}', '{1}')".format(rif.get(), nom_c.get())

                try:
                    fcursor.execute(sql)
                    bd.commit()
                except:
                    bd.rollback()
                    messagebox.showinfo(message="Hubo un error al registrar los datos del cliente", title="Aviso")

                lista_item = tabla_prod.get_children()
                for item in lista_item:
                    cant = tabla_prod.item(item)['text'],
                    producto = tabla_prod.item(item)['values'][0],
                    descto = tabla_prod.item(item)['values'][1]

                    p = producto[0]

                    sql = "SELECT idprod FROM producto WHERE producto = '"+p+"'"
                    
                    try:
                        fcursor.execute(sql)
                        id_p = fcursor.fetchall()
                    except:
                        bd.rollback()
                        messagebox.showinfo(message="No existen registros", title="Aviso")

                    pp = 200

                    pD = float(pp) * float(descto) / 100
                    ptp = cant * (pp - pD)

                    sql="INSERT INTO prod/factura (id_producto,cantidad,descuento, precio_tp) VALUES ('{0}', '{1}', '{2}', '{3}')".format(id_p, cant, descto, ptp)
                    try:
                        fcursor.execute(sql)
                        bd.commit()
                    except:
                        bd.rollback()
                        messagebox.showinfo(message="Hubo un error al registrar los productos", title="Aviso")

                bd.close()
            else: 
                messagebox.showinfo(title="Aviso", message="Debe ingresar mínimo un producto a la factura")
        else: 
            messagebox.showinfo(title="Aviso", message="Debe ingresar los datos del cliente")

    boton3 = Button(pantalla3, text="Generar factura", command=generar_factura)
    boton3.grid(row=18,column=2)

def mostrar_p():
    tp = list()
    lista = listar_prod()
    option_var = StringVar(pantalla3)
    
    if lista:
        for p in lista:
            tp.append(p)

        option_menu = ttk.OptionMenu(
            pantalla3,
            option_var,
            tp[0],
            *tp)
        option_menu.grid(row=6,column=1)
        option_menu.config(width=30)
    else: 
        c_np = Label (pantalla3, text="No hay productos registrados")
        c_np.grid(row=6,column=1)

def factura():
    global pantalla5
    pantalla5 = Toplevel(pantalla1)
    pantalla5.geometry("400x250")
    pantalla5.title("Facturación")
    pantalla5.iconbitmap("icono.ico")

    c1 = Label (pantalla5, text="Facturas Realizadas", fg="black", height="3", font=("sans serif", 15))
    c1.grid(row=2,column=0, columnspan=5)

def registrar_p():
    global pantalla4
    pantalla4 = Toplevel(pantalla1)
    pantalla4.geometry("400x350")
    pantalla4.title("Registrar Productos")
    pantalla4.iconbitmap("icono.ico")

    Label (pantalla4, text="Por favor ingrese los datos del producto" , fg="black", width="300", height="3", font=("sans serif", 15)).pack()
    Label (pantalla4, text="").pack()

    global nombre_p, precio

    Label (pantalla4, text="Nombre del producto").pack()
    nombre_p= Entry(pantalla4)
    nombre_p.pack()
    Label (pantalla4).pack()

    Label (pantalla4, text="Precio").pack()
    precio= Entry(pantalla4)
    precio.pack()
    Label (pantalla4).pack()

    Button(pantalla4, text="Registrar", command= registro_pdb).pack()

def registro_pdb():
    
    bd = pymysql.connect(
        host = "localhost",
        user="root",
        passwd="",
        db="bd"
    )

    if len(nombre_p.get()) != 0 and len(precio.get()) != 0:

            fcursor=bd.cursor()

            sql="INSERT INTO producto (producto, precio) VALUES ('{0}', '{1}')".format(nombre_p.get(), precio.get())

            try:
                fcursor.execute(sql)
                bd.commit()
                messagebox.showinfo(message="Registro Exitoso", title="Aviso")
                mostrar_p()
            except:
                bd.rollback()
                messagebox.showinfo(message="No registrado", title="Aviso")

            bd.close()

    else: 
        messagebox.showinfo(title="Aviso", message="Los campos son obligatorios")

def listar_prod():
    bd = pymysql.connect(
        host = "localhost",
        user="root",
        passwd="",
        db="bd"
    )

    fcursor=bd.cursor()

    lista_p = []
    sql="SELECT producto FROM producto"

    try:
        fcursor.execute(sql)
        lista_p= fcursor.fetchall()
        bd.commit()
        bd.close()
    except:
        bd.rollback()
        messagebox.showinfo(message="No se han encontrado registros", title="Aviso")
        bd.close()
    return lista_p    

def toggle_password_visibility():

    if contrasena_entry.cget('show') == '':
        contrasena_entry.config(show='*')

    else:
        contrasena_entry.config(show='')

def guardar_factura():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Factura #", ln=True)
    pdf.cell(200, 10, f"Usuario: ", ln=True)
    pdf.cell(200, 10, f"RIF Cliente:", ln=True)
    pdf.cell(200, 10, f"Productos: ", ln=True)
    pdf.cell(200, 10, f"Fecha Creacion: ", ln=True)
    pdf.cell(200, 10, f"Subtotal: ", ln=True)
    pdf.cell(200, 10, f"IVA: ", ln=True)
    pdf.cell(200, 10, f"Descuento: ", ln=True)
    pdf.cell(200, 10, f"Total: ", ln=True)
    pdf.output(f"factura_.pdf")
            
menu_pantalla()