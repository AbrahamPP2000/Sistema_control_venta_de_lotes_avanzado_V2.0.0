# # Ruta de la carpeta con los archivos CSV
# folder = "C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV"
#
# # Lista todos los archivos en la carpeta
# files = os.listdir(folder)

######################################################

# import chardet
#
# # Abrir el archivo en modo binario para detectar la codificación
# with open(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv", 'rb') as file:
#     raw_data = file.read()
#     result = chardet.detect(raw_data)
#     encoding = result['encoding']
#
# print(f"La codificación detectada es: {encoding}")

######################################################

# import pandas as pd

# Leer el archivo CSV con la codificación original
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv", encoding='ascii')
# print(df)
# # Guardar el archivo CSV con la nueva codificación
# df.to_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\AbonosASCII.csv", encoding='ascii', index=False)

######################################################

# import requests
# from bs4 import BeautifulSoup
#
# # URL de Google Finance para el tipo de cambio USD/MXN
# url = "https://www.google.com/finance/quote/USD-MXN"
#
# # Hacemos una solicitud GET a la página
# response = requests.get(url)
#
# # Verificamos que la solicitud fue exitosa
# if response.status_code == 200:
#     # Parseamos el contenido HTML de la página
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Extraemos el valor del tipo de cambio usando el selector adecuado
#     price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
#
#     if price_element:
#         # Obtenemos el texto del elemento
#         exchange_rate = price_element.text
#         print(f"El tipo de cambio actual de USD a MXN es: {exchange_rate}")
#     else:
#         print("No se pudo encontrar el tipo de cambio en la página.")
# else:
#     print(f"Error al acceder a la página: {response.status_code}")
#
# from datetime import datetime
#
# # Obtener la fecha y hora actuales
# fecha_actual = datetime.now()
#
# # # Formatear la fecha en el formato: Día-Mes-Año Hora:Minuto:Segundo
# # fecha_formateada = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
#
# # Formatear la fecha en el formato: Año-Mes-Día
# fecha_formateada = fecha_actual.strftime("%Y-%d-%m")
#
# # Mostrar la fecha formateada
# print("Fecha formateada:", fecha_formateada)

######################################################

# Leer el archivo CSV con pandas

# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Balance.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Compras.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv") # Ya importado
# print(df)
# Crear una consulta SQL para insertar los datos
# for _, row in df.iterrows():
# sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados)  # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Clientes (IdCliente, Nombre, Domicilio, Telefono) # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Dolar (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Compras (NoManzana, NoLote, CostoPorMetroCuadrado, ImporteTotal, Fecha, IdCliente, FormaDePago) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Balance (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, CantidadAbonada, NoRecibo, Saldo) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""

######################################################

# cursor.execute(sql, tuple(row))
# cursor.execute("delete from Gestion_de_lotes.Balance where IdBalance = 1 ")

# Consulta de datos en una tabla.
# consulta = "select * from Gestion_de_lotes.Abonos"
# cursor.execute(consulta)
# info = cursor.fetchall()
# for registro in info:
#     print(registro)

######################################################

# Obtención de un resultado a partir de una operación
# consulta = "SELECT SUM(ImporteTotal) FROM Gestion_de_lotes.Compras"
# # Ejecutar la consulta
# cursor.execute(consulta)
#
# # Obtener el resultado de la suma
# resultado = cursor.fetchone()
#
# # Imprimir el resultado
# print(f"La suma de los importes es: {resultado[0]}")

######################################################


# import mysql.connector  # Para la conexión con la base de datos MySQL
# from mysql.connector import Error  # Para manejar errores de conexión
#
# # Conectar a la base de datos MySQL
# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         database='gestion_de_lotes',
#         user='root',
#         password='mysql24$^ui(yuAs'
#     )
#
#     if connection.is_connected():  # Si la conexión ha sido exitosa
#         cursor = connection.cursor()
#         # connection.autocommit = False
#         # Realizar un cambio en la base de datos
#         consulta = f"SELECT * from Gestion_de_lotes.Prueba Where NUMERO1 = 1"
#         cursor.execute(consulta)
#
#         resultado = cursor.fetchall()
#         print(resultado)
#
#         # Confirmar temporalmente el cambio para que sea visible
#         connection.commit()  # Esto es necesario para que los cambios sean visibles
#         # # Espera la entrada del usuario
#         # print("Funciona?")
#         # input()  # El programa se detendrá hasta que el usuario presione Enter
#         #
#         # # Revertir los cambios, deshacer lo hecho
#         # query = "UPDATE Gestion_de_lotes.Prueba SET NUMERO2 = 99 WHERE NUMERO1 = 1"  # Esto revertirá el cambio realizado por el UPDATE
#         # cursor.execute(query)
#         # connection.commit()
#         # print("Los cambios han sido revertidos. La base de datos ha vuelto a su estado original.")
#
#         cursor.close()
#         connection.close()
#         print("Conexión a MySQL cerrada")
#
# except Error as e:
#     print("(1)Error al conectar a MySQL", e)
######################################################
# import inspect
#

# class MiClase:
#     def funcion_a(self):
#         self.funcion_compartida()
#
#     def funcion_b(self):
#         self.funcion_compartida()
#
#     def terceras(self):
#         self.funcion_compartida()
#
#     def funcion_compartida(self):
#         llamador = inspect.stack()[1].function
#         if llamador == "funcion_a":
#             print("Código para 'funcion_a'")
#         elif llamador == "funcion_b":
#             print("Código para 'funcion_b'")
#         elif llamador == "terceras":
#             print("Terceras")
#
# obj = MiClase()
# obj.funcion_a()  # Salida: Código para 'funcion_a'
# obj.funcion_b()  # Salida: Código para 'funcion_b'
# obj.terceras()
#######################################################################################################################
# import csv
# import subprocess
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import mysql.connector
# from mysql.connector import Error
# from Expert_System import ExpertSystem
# from Payment_Options import PaymentOptions
#
# # Importar bibliotecas de Tkinter
# import tkinter as tk
# from tkinter import ttk
#
# # Crear la ventana principal
# root = tk.Tk()
# root.title("Gestión de Lotes")
#
# # Crear frames para organizar los elementos
# frame_menu = ttk.Frame(root, padding="10")
# frame_menu.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#
# frame_content = ttk.Frame(root, padding="10")
# frame_content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#
# # Variables para almacenar los datos ingresados por el usuario
# var_manzana = tk.StringVar()
# var_lote = tk.StringVar()
# var_cliente = tk.StringVar()
# var_precio_metro = tk.StringVar()
#
# # Funciones básicas (se omiten las modificaciones por brevedad)
# ...
#
#
# def lot_purchase(cursor):
#     # Limpiar el frame de contenido
#     for widget in frame_content.winfo_children():
#         widget.destroy()
#
#     # Mostrar la lista de lotes disponibles
#     label_lotes = ttk.Label(frame_content, text="Lista de lotes disponibles:")
#     label_lotes.grid(row=0, column=0, columnspan=2, sticky=tk.W)
#
#     # Consulta para obtener la información de los lotes disponibles
#     query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
#     cursor.execute(query)
#     info = cursor.fetchall()
#     columns = cursor.column_names
#
#     # Mostrar la información en una tabla
#     tabla_lotes = ttk.Treeview(frame_content, columns=columns, show="headings")
#     for col in columns:
#         tabla_lotes.heading(col, text=col)
#     for row in info:
#         tabla_lotes.insert("", tk.END, values=row)
#     tabla_lotes.grid(row=1, column=0, columnspan=2)
#
#     # Campos para ingresar los datos del lote a comprar
#     label_manzana = ttk.Label(frame_content, text="Número de manzana:")
#     label_manzana.grid(row=2, column=0, sticky=tk.W)
#     entry_manzana = ttk.Entry(frame_content, textvariable=var_manzana)
#     entry_manzana.grid(row=2, column=1)
#
#     label_lote = ttk.Label(frame_content, text="Número de lote:")
#     label_lote.grid(row=3, column=0, sticky=tk.W)
#     entry_lote = ttk.Entry(frame_content, textvariable=var_lote)
#     entry_lote.grid(row=3, column=1)
#
#     label_precio = ttk.Label(frame_content, text="Precio por metro cuadrado:")
#     label_precio.grid(row=4, column=0, sticky=tk.W)
#     entry_precio = ttk.Entry(frame_content, textvariable=var_precio_metro)
#     entry_precio.grid(row=4, column=1)
#
#     # Botón para proceder con la compra
#     def proceder_compra():
#         # Obtener los valores ingresados por el usuario
#         no_manzana = var_manzana.get()
#         no_lote = var_lote.get()
#         precio_metro = var_precio_metro.get()
#
#         # Realizar las operaciones necesarias para procesar la compra
#         ...
#
#     button_proceder = ttk.Button(frame_content, text="Proceder con la compra", command=proceder_compra)
#     button_proceder.grid(row=5, column=0, columnspan=2)
#
#
# def main_menu(cursor):
#     # Limpiar el frame de contenido
#     for widget in frame_content.winfo_children():
#         widget.destroy()
#
#     # Botones del menú principal
#     button_compra = ttk.Button(frame_menu, text="Iniciar la compra de lote", command=lambda: lot_purchase(cursor))
#     button_compra.grid(row=0, column=0, sticky=(tk.W, tk.E))
#
#     button_consulta_lote = ttk.Button(frame_menu, text="Consultar un lote", command=lambda: lot_consultation(cursor))
#     button_consulta_lote.grid(row=1, column=0, sticky=(tk.W, tk.E))
#
#     button_sumatoria_finiquitados = ttk.Button(frame_menu, text="Consultar la sumatoria de los importes finiquitados",
#                                                command=lambda: sum_of_settled_amounts(cursor))
#     button_sumatoria_finiquitados.grid(row=2, column=0, sticky=(tk.W, tk.E))
#
#     button_sumatoria_abonos = ttk.Button(frame_menu,
#                                          text="Consultar la sumatoria de los abonos de los lotes en proceso de compra",
#                                          command=lambda: sum_of_payments_for_lots_to_be_sold(cursor))
#     button_sumatoria_abonos.grid(row=3, column=0, sticky=(tk.W, tk.E))
#
#     button_consulta_saldo = ttk.Button(frame_menu, text="Consultar el saldo de un lote",
#                                        command=lambda: balance_consultation(cursor))
#     button_consulta_saldo.grid(row=4, column=0, sticky=(tk.W, tk.E))
#
#     button_consulta_cliente = ttk.Button(frame_menu, text="Consultar los datos de un cliente",
#                                          command=lambda: client_consultation(cursor))
#     button_consulta_cliente.grid(row=5, column=0, sticky=(tk.W, tk.E))
#
#     button_salir = ttk.Button(frame_menu, text="Salir", command=root.quit)
#     button_salir.grid(row=6, column=0, sticky=(tk.W, tk.E))
#
#
# # Función principal
# def main():
#     try:
#         connection = sql_connection()
#     except Error as e:
#         print("Error al conectar a MySQL", e)
#         return
#
#     if connection.is_connected():
#         cursor = connection.cursor()
#         update_dollar_price(cursor)
#         main_menu(cursor)
#
#         # Iniciar el loop principal de la ventana
#         root.mainloop()
#
#         connection.commit()
#         cursor.close()
#         connection.close()
#         print("Conexión a MySQL cerrada")
#
#
# if _name_ == "_main_":
#     main()
#######################################################################################################################
# @staticmethod
# def payment_by_installments(cursor, lote, manzana, sqm_price, lot_price, client_id):
#     current_date = datetime.now()  # Fecha y hora actuales
#     formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
#     print(f"Fecha: {formatted_date}\n")  # Impresión de la fecha actual al momento de ingresar un abono
#     from Data_Import_and_processing import \
#         get_connection  # Se importa la instancia de la conexión de la base de datos para el guardado de los cambios
#     connection = get_connection()  # Obtención de la sesión correspondiente
#
#     # ... (código existente) ...
#
#     else:  # Si no hay ningún registro del lote correspondiente en la tabla Abonos, significa que la compra apenas comienza y se pagará un anticipo
#     while True:  # Bucle para pedir el anticipo y el número de recibo en caso de que se ingresen datos inválidos
#         try:
#             # Ingreso del pago de anticipo
#             partial_payment = float(input("Ingrese el anticipo que se pagó: $"))
#             balance = lot_price - partial_payment  # Cálculo del saldo restante
#             receipt_number = int(input("Ingrese el número de recibo: "))  # Ingreso del número de recibo
#             # Inserción del anticipo a la tabla "Abonos"
#             insert_query = (
#                 f"INSERT INTO gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, CantidadAbonada, NoRecibo, Saldo) VALUES (\'{formatted_date}\', {manzana}, {lote}, 1, {partial_payment}, {receipt_number}, {balance})")
#
#             cursor.execute(insert_query)  # Ejecución de la consulta
#             connection.commit()  # Guardado de los cambios en la base de datos
#
#             # Verificar si el saldo es cero después del abono
#             if balance == 0:
#                 # Actualizar el estado del lote a "Comprado"
#                 lot_data_update = (
#                     f"UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = {sqm_price}, PrecioTotal = {lot_price}, Estatus = 'Comprado' WHERE NoManzana = {manzana} AND NoLote = {lote}")
#                 cursor.execute(lot_data_update)  # Ejecución de la operación
#                 connection.commit()  # Guardado de los cambios
#
#                 # Llamar a la función purchase_table_row_insertion para registrar la compra
#                 PaymentOptions.purchase_table_row_insertion(connection, cursor, lote, manzana, sqm_price, lot_price,
#                                                             client_id)
#             else:
#                 # Operación en donde se edita el registro correspondiente al lote
#                 lot_data_update = (
#                     f"UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = {sqm_price}, PrecioTotal = {lot_price}, Estatus = 'En proceso de compra' WHERE NoManzana = {manzana} AND NoLote = {lote}")
#                 cursor.execute(lot_data_update)  # Ejecución de la operación
#                 connection.commit()  # Guardado de los cambios
#
#             break  # Salida del bucle en caso de que el anterior código haya funcionado correctamente
#         except ValueError:  # Si el usuario ingresó un dato inválido
#             print("Ingrese datos válidos.")  # Mensaje de error correspondiente


