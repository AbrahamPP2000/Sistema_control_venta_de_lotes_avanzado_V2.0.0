import csv  # Para el manejo de archivos CSV a la hora de importar datos
import pandas as pd  # Para el formato de la información a la hora de imprimir detalles de la base de datos
import requests  # Para acceder a la página web Google Finance para obtener el precio del dólar
from bs4 import BeautifulSoup  # Para la revisión y extracción de información de archivos html y xml de páginas web
from datetime import datetime  # Para la extracción de la fecha actual del sistema operativo a la hora de actualizar
# el precio del dólar
import mysql.connector  # Para la conexión con la base de datos MySQL
from mysql.connector import Error  # Para lanzar un mensaje de error en caso de no poder acceder a la base de datos
from Payment_Options import PaymentOptions  # Clase del proyecto en donde están las formas posibles de pago
from Sales_assistant import LotSalesAssistant  # Importación del asistente de compras
import tkinter as tk  # Importación de la biblioteca necesaria para las interfaces
from tkinter import ttk, messagebox  # Importación de los elementos de las interfaces para los mensajes
from ttkthemes import ThemedTk  # Módulo para obtener temas visuales adicionales para las interfaces

# Abraham Pelayo Pinedo
# Centro Universitario de Ciencias Exactas e Ingenierías - Universidad de Guadalajara
# Código de estudiante: 215500336
# Ingeniería en Computación
# 2025A

# Título del proyecto modular: "Sistema de control de venta de lotes avanzado"
# ("Advanced land lot sales control system")

"""Nota 1: Los comentarios en donde hay funciones "print" e "input" se dejaron en el código por razones de diseño.
Se identifican con tres "-" antes de la línea y después del numeral "#" """

"""Nota 2: El código está escrito enteramente en inglés mientras que los comentarios que documentan su 
funcionamiento están enteramente en español."""


# Funciones básicas

def update_dollar_price(cursor):  # Actualización del precio del dólar cada vez que se ejecuta el programa
    current_date = datetime.now()  # Obtención de la fecha y hora actuales
    formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha de la siguiente manera: Año-Mes-Día
    url = "https://www.google.com/finance/quote/USD-MXN"  # URL de Google Finance para el tipo de cambio USD/MXN
    response = requests.get(url)  # Hacemos una solicitud GET a la página
    if response.status_code == 200:  # Verificamos que la solicitud fue exitosa en base del código de estatus HTTP
        soup = BeautifulSoup(response.content, 'html.parser')  # Parseamos el contenido HTML de la página
        price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})  # Extraemos el valor del tipo de cambio
        # usando el selector adecuado
        if price_element:  # Si efectivamente hay un dato en el campo buscado previamente
            global exchange_rate  # Ponemos la variable en donde se almacena el valor del dólar como global para su
            # fácil acceso
            exchange_rate = price_element.text  # Obtenemos el texto del elemento
            # --- print("Actualizando precio del dólar...")
            status_window = tk.Toplevel()  # Generación de la interfaz
            status_window.title("Actualización del Dólar")  # Título de la interfaz
            # Etiqueta de la interfaz que indica la actualización del precio del dólar
            status_label = ttk.Label(status_window, text="Actualizando precio del dólar...")
            # Ajuste de la ubicación de la etiqueta dentro de la interfaz
            status_label.pack(padx=20, pady=10)
            # Se actualiza el valor del campo correspondiente de la tabla del dólar en la base de datos
            dollar_price_query = (f"UPDATE gestion_de_lotes.dolar SET Fecha = '{formatted_date}', "
                                  f"PrecioEnPesos = {exchange_rate} LIMIT 1")
            cursor.execute(dollar_price_query)  # Ejecución de la consulta
            connection.commit()  # Aplicación de los cambios
            # Ruta del archivo CSV del dólar
            dollar_file_route = r'C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv'
            try:
                # Lectura del archivo CSV y almacenamiento de las filas
                with open(dollar_file_route, mode='r', newline='') as csv_file:
                    reader_csv = csv.reader(csv_file)  # Generación de un objeto para leer un archivo CSV
                    rows = list(reader_csv)  # Conversión del contenido a una lista para modificarlo
                # Modificación de la primera fila con los nuevos datos
                rows[1] = [formatted_date, exchange_rate]  # Modifica la fila 1 (índice 0 suele ser el encabezado)
                # Se escribe el archivo CSV con las filas actualizadas
                with open(dollar_file_route, mode='w', newline='') as csv_file:
                    writer_csv = csv.writer(csv_file)  # Generación de un objeto para escribir en un archivo CSV
                    writer_csv.writerows(rows)  # Se sobrescribe el archivo con las filas modificadas
                # --- print("Precio del dólar actualizado con éxito en la base de datos y en el CSV.")
                # Etiqueta que indica el éxito de la operación
                success_label = ttk.Label(status_window,
                                          text="Precio del dólar actualizado con éxito en la base de datos y en el CSV.")
                success_label.pack(padx=20, pady=10)  # Ajuste de la ubicación de la etiqueta en la interfaz
                status_window.after(2000, status_window.destroy)  # Eliminación de la ventana para liberar memoria
            except FileNotFoundError:  # Si el archivo no ha sido encontrado en la ruta especificada
                # --- print("Archivo no encontrado.")
                # Mensaje de error correspondiente
                messagebox.showerror("Error", "Archivo no encontrado.")
        else:  # Si no hay un dato en el campo accedido durante el webscraping
            # --- print("No se pudo encontrar el tipo de cambio en la página.")
            # Mensaje de error correspondiente
            messagebox.showerror("Error", "No se pudo encontrar el tipo de cambio en la página.")
    else:  # Si no se pudo acceder a la página
        # --- print(f"Error al acceder a la página: {response.status_code}")
        # Mensaje de error correspondiente
        messagebox.showerror("Error", f"Error al acceder a la página: {response.status_code}")


def sum_of_settled_amounts(cursor):
    # Consulta correspondiente para la suma de los importes finiquitados
    query = "SELECT SUM(PrecioTotal) FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Comprado'"
    cursor.execute(query)  # Ejecutar la consulta
    result = cursor.fetchone()  # Obtener el resultado de la suma

    # Creación de la ventana para mostrar resultados
    result_window = tk.Toplevel()
    # Título de la ventana
    result_window.title("Suma de Importes Finiquitados")

    # Frame o marco para organizar contenido
    frame = ttk.Frame(result_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Mostrar resultado bruto en otra etiqueta
    # --- print(f"Resultado bruto: {result}")
    raw_result_label = ttk.Label(frame, text=f"Resultado bruto: {result}")
    raw_result_label.pack(pady=10)

    # Mostrar resultado formateado
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado bruto
    # --- print(f"La suma de los importes es: {formatted_result}\n")
    # Etiqueta para mostrar la suma de los importes
    formatted_result_label = ttk.Label(frame,
                                       text=f"La suma de los importes es: {formatted_result}",
                                       font=("Arial", 12, "bold"))
    formatted_result_label.pack(pady=10)

    # Botón para cerrar
    close_button = ttk.Button(frame, text="Cerrar", command=result_window.destroy)
    close_button.pack(pady=10)


def sum_of_payments_for_lots_to_be_sold(cursor):
    # Consulta SQL de la suma de los abonos de los lotes en proceso de compra
    query = "SELECT SUM(CantidadAbonada) FROM Gestion_de_lotes.Abonos"
    cursor.execute(query)  # Ejecución de la consulta
    result = cursor.fetchone()  # Obtención del resultado de la suma

    # Crear ventana para mostrar resultados
    result_window = tk.Toplevel()
    # Título de la ventana
    result_window.title("Suma de Abonos")

    # Frame para organizar contenido
    frame = ttk.Frame(result_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Mostrar resultado bruto con una etiqueta
    # --- print(f"Resultado bruto: {result}")
    raw_result_label = ttk.Label(frame, text=f"Resultado bruto: {result}")
    raw_result_label.pack(pady=10)

    # Mostrar resultado formateado
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado de la suma
    # --- print(f"La suma de los abonos es: {formatted_result}")
    # Etiqueta para poner el resultado formateado
    formatted_result_label = ttk.Label(frame,
                                       text=f"La suma de los abonos es: {formatted_result}",
                                       font=("Arial", 12, "bold"))
    formatted_result_label.pack(pady=10)

    # Botón para cerrar
    close_button = ttk.Button(frame, text="Cerrar", command=result_window.destroy)
    close_button.pack(pady=10)


def client_consultation(cursor):
    client_window = tk.Toplevel()  # Creación de la ventana para la consulta de clientes
    client_window.title("Consulta de Clientes")  # Título de la ventana
    client_window.geometry("800x600")  # Tamaño de la ventana

    # Frame principal
    main_frame = ttk.Frame(client_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta para poner el texto "Clientes registrados:"
    # --- print("Clientes registrados: \n")
    ttk.Label(main_frame, text="Clientes registrados:", font=("Arial", 12, "bold")).pack(pady=10)

    # Consulta para obtener los ID y los nombres
    query = "SELECT IdCliente, Nombre FROM Gestion_de_lotes.Clientes"
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de cada uno de los registros de la tabla

    # Crear Treeview para mostrar clientes
    tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre'), show='headings')
    tree.heading('ID', text='ID Cliente')
    tree.heading('Nombre', text='Nombre')

    # Inserción de cada uno de los registros de la consulta al Treeview
    for row in info:
        tree.insert('', tk.END, values=row)

    # Ajuste del Treeview
    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Frame para entrada de ID
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)

    # Generación de la etiqueta "ID del cliente:"
    ttk.Label(input_frame, text="ID del cliente:").pack(side=tk.LEFT, padx=5)
    id_entry = ttk.Entry(input_frame)
    id_entry.pack(side=tk.LEFT, padx=5)

    # Función anidada para mostrar los detalles del cliente que se quiere consultar
    def show_client_details():
        try:
            client_id = id_entry.get()  # Se obtiene el ID del campo de entrada correspondiente
            if client_id.isnumeric() and int(client_id) < (len(info) + 1):  # Si lo que digitó el usuario es un número
                # y está en el rango del número disponible de registros en la tabla
                # Consulta auxiliar para imprimir los datos del cliente especificado
                auxQuery = f"SELECT * FROM Gestion_de_lotes.Clientes WHERE IdCliente = {client_id}"
                cursor.execute(auxQuery)  # Ejecución de la consulta auxiliar
                client_info = cursor.fetchall()  # Obtención del resultado

                # Mostrar detalles en una nueva ventana
                details_window = tk.Toplevel()
                details_window.title(f"Detalles del Cliente {client_id}")

                # Crear Treeview para mostrar detalles del cliente
                details_tree = ttk.Treeview(details_window,
                                            columns=('ID', 'Nombre', 'Domicilio', 'Teléfono'),
                                            show='headings')
                details_tree.heading('ID', text='ID')
                details_tree.heading('Nombre', text='Nombre')
                details_tree.heading('Domicilio', text='Domicilio')
                details_tree.heading('Teléfono', text='Teléfono')

                # Bucle para insertar los datos del cliente a la interfaz
                for info_row in client_info:
                    details_tree.insert('', tk.END, values=info_row)
                details_tree.pack(padx=20, pady=20)
            else:  # Si el ID no existe en la tabla
                # Mensaje de error correspondiente
                messagebox.showerror("Error", "El cliente no existe, intente de nuevo.")
        except ValueError:  # Si lo que digitó el usuario dentro del campo de solicitud de ID no ayuda a
            # identificar un registro
            # Mensaje de error correspondiente
            messagebox.showerror("Error", "Opción no válida. Intente de nuevo.")
    # Botón para ver los detalles del cliente después de haber ingresado su ID
    ttk.Button(input_frame, text="Consultar", command=show_client_details).pack(side=tk.LEFT, padx=5)
    # Botón para cerrar la ventana de la consulta de cliente
    ttk.Button(main_frame, text="Cerrar", command=client_window.destroy).pack(pady=10)


def lot_consultation(cursor):
    # Crear ventana para consulta de lotes
    lot_window = tk.Toplevel()
    lot_window.title("Consulta de Lotes")

    # Frame principal
    main_frame = ttk.Frame(lot_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frames para entrada de datos
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)

    # Diseño del campo para ingresar el número de lote
    ttk.Label(input_frame, text="Número de lote:").grid(row=0, column=0, padx=5, pady=5)
    lot_entry = ttk.Entry(input_frame)
    lot_entry.grid(row=0, column=1, padx=5, pady=5)

    # Diseño del campo para ingresar el número de manzana
    ttk.Label(input_frame, text="Número de manzana:").grid(row=1, column=0, padx=5, pady=5)
    block_entry = ttk.Entry(input_frame)
    block_entry.grid(row=1, column=1, padx=5, pady=5)

    # Diseño del frame para mostrar resultados
    result_frame = ttk.Frame(main_frame)
    result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Función anidada para poder llevar a cabo consultas cuantas veces quiera el usuario
    def show_lot_details():
        # Limpiar resultados anteriores
        for widget in result_frame.winfo_children():
            widget.destroy()

        lot_number = lot_entry.get()  # Se obtiene el número de lote
        block_number = block_entry.get()  # Se obtiene el número de manzana

        # Consulta para obtener la información correspondiente
        query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = " + block_number + " and NoLote = " + lot_number
        cursor.execute(query)  # Ejecución de la consulta
        info = cursor.fetchall()  # Obtención de los datos del lote

        # Crear Treeview para mostrar detalles
        columns = ('NoManzana', 'NoLote', 'Direccion', 'MtsCuadrados', 'CostoMetroCuadrado', 'PrecioTotal', 'Estatus')
        tree = ttk.Treeview(result_frame, columns=columns, show='headings')

        # Configurar encabezados
        headers = ['No. Manzana', 'No. Lote', 'Dirección', 'Metros²', 'Costo/m²', 'Precio Total', 'Estatus']
        for col, header in zip(columns, headers):
            tree.heading(col, text=header)
            tree.column(col, width=100)  # Ajustar según necesidades

        # Insertar datos
        for row in info:  # Inserción de los datos del lote al Treeview
            tree.insert('', tk.END, values=row)
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)
    # Botón para ver los detalles del lote después de haber ingresado los datos necesarios
    ttk.Button(button_frame, text="Consultar", command=show_lot_details).pack(side=tk.LEFT, padx=5)
    # Botón para cerrar la ventana de la consulta de lotes
    ttk.Button(button_frame, text="Cerrar", command=lot_window.destroy).pack(side=tk.LEFT, padx=5)


def info_adjustment(cursor, connection):
    # Crear ventana para ajuste de información
    adjust_window = tk.Toplevel()
    adjust_window.title("Ajuste de Información")

    # Frame principal
    main_frame = ttk.Frame(adjust_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Función anidada para hacer la operación de ajuste cuantas veces se quiera
    def load_and_display_data():
        # Ruta del archivo CSV
        df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")

        # Mostrar datos en Treeview
        tree = ttk.Treeview(main_frame, columns=list(df.columns), show='headings')

        # Configurar encabezados
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insertar datos
        for index, row in df.iterrows():
            tree.insert('', tk.END, values=list(row))

            # Consulta para insertar los datos en la tabla correspondiente
            sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados, CostoMetroCuadrado,
            PrecioTotal, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, tuple(row))  # Ejecución de la consulta
            connection.commit()  # Guardado de los cambios en la base de datos

        tree.pack(pady=20, fill=tk.BOTH, expand=True)
        # Mensaje de éxito de la operación
        messagebox.showinfo("Éxito", "Datos cargados y actualizados correctamente")

    # Botón para proceder con la operación
    ttk.Button(main_frame, text="Cargar Datos", command=load_and_display_data).pack(pady=10)
    # Botón para salir del proceso
    ttk.Button(main_frame, text="Cerrar", command=adjust_window.destroy).pack(pady=10)


def lot_purchase(cursor):
    # Crear ventana principal para compra de lotes
    purchase_window = tk.Toplevel()
    purchase_window.title("Compra de Lotes")
    purchase_window.geometry("1000x800")

    # Frame principal
    main_frame = ttk.Frame(purchase_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main_frame, text="Lista de lotes disponibles:", font=("Arial", 12, "bold")).pack(pady=10)

    # Mostrar lotes disponibles
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
    cursor.execute(query)
    info = cursor.fetchall()
    columns = cursor.column_names

    # Crear Treeview para mostrar lotes
    tree = ttk.Treeview(main_frame, columns=columns, show='headings')

    # Configurar columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Insertar datos
    for row in info:
        tree.insert('', tk.END, values=row)

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Frame para entrada de datos
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)

    ttk.Label(input_frame, text="Número de manzana:").grid(row=0, column=0, padx=5, pady=5)
    block_entry = ttk.Entry(input_frame)
    block_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Número de lote:").grid(row=1, column=0, padx=5, pady=5)
    lot_entry = ttk.Entry(input_frame)
    lot_entry.grid(row=1, column=1, padx=5, pady=5)

    def process_purchase():
        no_manzana = int(block_entry.get())
        no_lote = int(lot_entry.get())

        # Obtener detalles del lote
        query = (f"SELECT MtsCuadrados, CostoMetroCuadrado, PrecioTotal FROM Gestion_de_lotes.Lotes WHERE NoManzana = "
                 f"{no_manzana} AND NoLote = {no_lote}")
        cursor.execute(query)
        lot_details = cursor.fetchone()

        if lot_details:
            # Crear ventana para precio por metro cuadrado
            price_window = tk.Toplevel()
            price_window.title("Precio por Metro Cuadrado")

            ttk.Label(price_window, text="Precio por metro cuadrado:").pack(pady=10)
            price_entry = ttk.Entry(price_window)
            price_entry.pack(pady=10)

            def process_price():
                try:
                    price_per_square_meter = float(price_entry.get())
                    price_window.destroy()

                    # Mostrar clientes registrados
                    aux_query = "SELECT Nombre FROM Gestion_de_lotes.Clientes"
                    cursor.execute(aux_query)
                    customer_names = [name[0] for name in cursor.fetchall()]

                    # Ventana para selección de cliente
                    client_window = tk.Toplevel()
                    client_window.title("Selección de Cliente")

                    ttk.Label(client_window, text="Clientes registrados:").pack(pady=10)
                    client_listbox = tk.Listbox(client_window, width=50)
                    for name in customer_names:
                        client_listbox.insert(tk.END, name)
                    client_listbox.pack(pady=10)

                    ttk.Label(client_window, text="Nombre del cliente:").pack(pady=5)
                    client_entry = ttk.Entry(client_window)
                    client_entry.pack(pady=5)

                    def process_client():
                        customer_name = client_entry.get()
                        if customer_name not in customer_names:
                            # Ventana para nuevo cliente
                            new_client_window = tk.Toplevel()
                            new_client_window.title("Nuevo Cliente")

                            ttk.Label(new_client_window, text="Domicilio:").pack(pady=5)
                            address_entry = ttk.Entry(new_client_window)
                            address_entry.pack(pady=5)

                            ttk.Label(new_client_window, text="Teléfono:").pack(pady=5)
                            phone_entry = ttk.Entry(new_client_window)
                            phone_entry.pack(pady=5)

                            def save_new_client():
                                address = address_entry.get()
                                phone_number = phone_entry.get()

                                client_insert_query = (
                                    f"INSERT INTO Gestion_de_lotes.Clientes (Nombre, Domicilio, Telefono) "
                                    f"VALUES (\'{customer_name}\', \'{address}\', \'{phone_number}\')")
                                cursor.execute(client_insert_query)
                                connection.commit()

                                id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \'{customer_name}\'"
                                cursor.execute(id_client_query)
                                client_id = cursor.fetchone()[0]

                                show_payment_options(no_lote, no_manzana, price_per_square_meter, client_id)
                                new_client_window.destroy()
                                client_window.destroy()

                            ttk.Button(new_client_window, text="Guardar", command=save_new_client).pack(pady=10)
                        else:
                            id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \'{customer_name}\'"
                            cursor.execute(id_client_query)
                            client_id = cursor.fetchone()[0]

                            show_payment_options(no_lote, no_manzana, price_per_square_meter, client_id)
                            client_window.destroy()

                    ttk.Button(client_window, text="Continuar", command=process_client).pack(pady=10)

                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido para el precio.")

            ttk.Button(price_window, text="Continuar", command=process_price).pack(pady=10)
        else:
            messagebox.showerror("Error", "Lote no encontrado.")

    def show_payment_options(no_lote, no_manzana, price_per_square_meter, client_id):
        payment_window = tk.Toplevel()
        payment_window.title("Opciones de Pago")

        ttk.Label(payment_window, text="Seleccione forma de pago:", font=("Arial", 12, "bold")).pack(pady=20)

        payment_method = PaymentOptions(connection)

        def process_payment(option):
            lot_data_query = f"SELECT MtsCuadrados FROM gestion_de_lotes.Lotes WHERE NoManzana = {no_manzana} AND NoLote = {no_lote}"
            cursor.execute(lot_data_query)
            square_meters = cursor.fetchone()[0]
            lot_price = price_per_square_meter * float(square_meters)

            if option == 1:
                payment_method.cash_payment(cursor, no_lote, no_manzana, price_per_square_meter, lot_price, client_id)
            elif option == 2:
                payment_method.payment_by_installments(cursor, no_lote, no_manzana, price_per_square_meter, lot_price,
                                                       client_id)
            elif option == 3:
                payment_method.payment_in_kind(cursor, no_lote, no_manzana, price_per_square_meter, lot_price,
                                               client_id)

            payment_window.destroy()

        ttk.Button(payment_window, text="De contado",
                   command=lambda: process_payment(1)).pack(pady=10)
        ttk.Button(payment_window, text="Anticipo, parcialidades",
                   command=lambda: process_payment(2)).pack(pady=10)
        ttk.Button(payment_window, text="En especie",
                   command=lambda: process_payment(3)).pack(pady=10)

    ttk.Button(input_frame, text="Proceder con la compra", command=process_purchase).grid(row=2, column=0, columnspan=2,
                                                                                          pady=20)
    ttk.Button(main_frame, text="Cerrar", command=purchase_window.destroy).pack(pady=10)


# [continúa en la siguiente parte debido a limitaciones de longitud...]
# [partes anteriores...]


def balance_consultation(cursor):
    # Crear ventana para consulta de saldo
    balance_window = tk.Toplevel()
    balance_window.title("Consulta de Saldo")

    # Frame principal
    main_frame = ttk.Frame(balance_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame para entrada de datos
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)

    ttk.Label(input_frame, text="Número de lote:").grid(row=0, column=0, padx=5, pady=5)
    lot_entry = ttk.Entry(input_frame)
    lot_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Número de manzana:").grid(row=1, column=0, padx=5, pady=5)
    block_entry = ttk.Entry(input_frame)
    block_entry.grid(row=1, column=1, padx=5, pady=5)

    # Frame para mostrar resultado
    result_frame = ttk.Frame(main_frame)
    result_frame.pack(pady=20)

    def show_balance():
        lot_number = lot_entry.get()
        block_number = block_entry.get()

        query = ("SELECT Saldo FROM Gestion_de_lotes.Abonos WHERE NoManzana = " + block_number + " and NoLote = " +
                 lot_number + " and NoAbono = (SELECT MAX(NoAbono) FROM Gestion_de_lotes.Abonos WHERE NoManzana = " +
                 block_number + " and NoLote = " + lot_number + ")")

        try:
            cursor.execute(query)
            balance = cursor.fetchone()

            # Limpiar resultado anterior
            for widget in result_frame.winfo_children():
                widget.destroy()

            if balance:
                result_text = f"El saldo del lote número {lot_number} de la manzana {block_number} es: ${balance[0]:,.2f}"
                ttk.Label(result_frame, text=result_text, font=("Arial", 12)).pack(pady=10)
            else:
                messagebox.showwarning("Advertencia", "No se encontró información para este lote")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en la consulta: {err}")

    # Botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Consultar", command=show_balance).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Cerrar", command=balance_window.destroy).pack(side=tk.LEFT, padx=5)


def recording_installment(cursor):
    # Crear ventana para registro de abonos
    installment_window = tk.Toplevel()
    installment_window.title("Registro de Abonos")
    installment_window.geometry("1000x800")

    # Frame principal
    main_frame = ttk.Frame(installment_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main_frame, text="Lotes en proceso de compra", font=("Arial", 12, "bold")).pack(pady=10)

    # Mostrar lotes en proceso de compra
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'En proceso de compra'"
    cursor.execute(query)
    info = cursor.fetchall()
    columns = cursor.column_names

    # Crear Treeview para mostrar lotes
    tree = ttk.Treeview(main_frame, columns=columns, show='headings')

    # Configurar columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Insertar datos
    for row in info:
        tree.insert('', tk.END, values=row)

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Frame para entrada de datos
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20)

    ttk.Label(input_frame, text="Número de manzana:").grid(row=0, column=0, padx=5, pady=5)
    block_entry = ttk.Entry(input_frame)
    block_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Número de lote:").grid(row=1, column=0, padx=5, pady=5)
    lot_entry = ttk.Entry(input_frame)
    lot_entry.grid(row=1, column=1, padx=5, pady=5)

    def process_installment():
        try:
            no_manzana = int(block_entry.get())
            no_lote = int(lot_entry.get())

            # Obtener datos del lote
            lot_query = f"SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = {no_manzana} AND NoLote = {no_lote}"
            cursor.execute(lot_query)
            lot_data = cursor.fetchall()

            if lot_data:
                lot_data = lot_data[0]
                price_per_square_meter = lot_data[4]
                lot_price = lot_data[5]

                # Obtener ID del cliente
                client_query = (f"SELECT IdComprador FROM Gestion_de_lotes.Abonos WHERE NoManzana = {no_manzana} "
                                f"AND NoLote = {no_lote}")
                cursor.execute(client_query)
                client_id = cursor.fetchone()

                if client_id:
                    client_id = client_id[0]
                    payment_method = PaymentOptions(connection)
                    payment_method.payment_by_installments(cursor, no_lote, no_manzana, price_per_square_meter,
                                                           lot_price, client_id)
                else:
                    messagebox.showerror("Error", "No se encontró información del comprador")
            else:
                messagebox.showerror("Error", "Lote no encontrado")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en la base de datos: {err}")

    ttk.Button(input_frame, text="Registrar Abono",
               command=process_installment).grid(row=2, column=0, columnspan=2, pady=20)
    ttk.Button(main_frame, text="Cerrar", command=installment_window.destroy).pack(pady=10)


def main_menu(cursor):
    # Crear ventana principal
    root = ThemedTk(theme="arc")  # Usando un tema moderno
    root.title("Sistema de Gestión de Lotes")
    root.geometry("800x600")

    # Frame principal
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Título
    title_label = ttk.Label(main_frame, text="Sistema de Gestión de Lotes",
                            font=("Arial", 16, "bold"))
    title_label.pack(pady=20)

    # Frame para botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(expand=True)

    # Estilo para los botones
    button_style = ttk.Style()
    button_style.configure('Menu.TButton', padding=10, width=40)

    # Funciones para los botones
    def create_menu_button(text, command):
        return ttk.Button(button_frame, text=text, command=command, style='Menu.TButton')

    # Crear botones del menú
    buttons = [
        ("Iniciar la compra de lote", lambda: lot_purchase(cursor)),
        ("Consultar un lote", lambda: lot_consultation(cursor)),
        ("Consultar sumatoria de importes finiquitados", lambda: sum_of_settled_amounts(cursor)),
        ("Consultar sumatoria de abonos", lambda: sum_of_payments_for_lots_to_be_sold(cursor)),
        ("Consultar saldo de un lote", lambda: balance_consultation(cursor)),
        ("Consultar datos de un cliente", lambda: client_consultation(cursor)),
        ("Modificar registro", lambda: info_adjustment(cursor, connection)),
        ("Chatear con asistente virtual", lambda: LotSalesAssistant().chat()),
        ("Registrar abono", lambda: recording_installment(cursor)),
        ("Salir", root.destroy)
    ]

    for text, command in buttons:
        btn = create_menu_button(text, command)
        btn.pack(pady=5)

    # Iniciar loop principal
    root.mainloop()


def sql_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='gestion_de_lotes',
            user='root',
            password='mysql24$^ui(yuAs'
        )
        return connection
    except Error as e:
        messagebox.showerror("Error de Conexión", f"Error al conectar a MySQL: {e}")
        return None


def get_connection():
    global connection
    try:
        if not connection.is_connected():
            connection = sql_connection()
        return connection
    except:
        messagebox.showerror("Error", "Error al obtener la conexión a la base de datos")
        return None


if __name__ == "__main__":
    try:
        connection = sql_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            update_dollar_price(cursor)
            main_menu(cursor)
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Información", "Conexión a MySQL cerrada")
    except Exception as e:
        messagebox.showerror("Error", f"Error en la aplicación: {e}")
