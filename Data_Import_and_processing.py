import csv  # Para el manejo de archivos CSV a la hora de importar datos
import subprocess  # Para limpiar la pantalla después de cada operación.
import pandas as pd  # Para el formato de la información a la hora de imprimir detalles de la base de datos
import requests  # Para acceder a la página web Google Finance para obtener el precio del dólar
from bs4 import BeautifulSoup  # Para la revisión y extracción de información de archivos html y xml de páginas web
from datetime import datetime  # Para la extracción de la fecha actual del sistema operativo a la hora de actualizar
# el precio del dólar
import mysql.connector  # Para la conexión con la base de datos MySQL
from mysql.connector import Error  # Para lanzar un mensaje de error en caso de no poder acceder a la base de datos
from OpcionesPago import OpcionesPago  # Clase del proyecto en donde están las formas posibles de pago
from Sales_assistant import LotSalesAssistant  # Nueva importación

# Abraham Pelayo Pinedo
# Centro Universitario de Ciencias Exactas e Ingenierías - Universidad de Guadalajara
# Código de estudiante: 215500336
# Ingeniería en Computación
# 2025A

# Título del proyecto modular: "Sistema de control de venta de lotes avanzado"
# ("Advanced land lot sales control system")


# Funciones básicas

def actualizar_precio_dolar(cursor):
    # Actualización del precio del dólar cada vez que se ejecuta el programa
    current_date = datetime.now()  # Fecha y hora actuales
    # formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
    url = "https://www.google.com/finance/quote/USD-MXN"  # URL de Google Finance para el tipo de cambio USD/MXN
    response = requests.get(url)  # Hacemos una solicitud GET a la página
    if response.status_code == 200:  # Verificamos que la solicitud fue exitosa
        soup = BeautifulSoup(response.content, 'html.parser')  # Parseamos el contenido HTML de la página
        price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})  # Extraemos el valor del tipo de cambio
        # usando el selector adecuado
        if price_element:  # Si efectivamente hay un dato en el campo buscado previamente
            global exchange_rate  # Ponemos la variable en donde se almacena el valor del dólar como global para la
            # inicialización del sistema experto.
            exchange_rate = price_element.text  # Obtenemos el texto del elemento
            print("Actualizando precio del dólar...")
            # Inserción de los datos correspondientes a la tabla del dólar en la base de datos
            dollar_price_query = (f"INSERT INTO gestion_de_lotes.dolar (Fecha, PrecioEnPesos) VALUES (%s, %s)")
            data = (current_date, exchange_rate)  # Ejecución de la consulta
            cursor.execute(dollar_price_query, data)  # Ejecución de la consulta
            conexion.commit()  # Aplicación de los cambios
            # Ruta del archivo CSV del dólar
            dollar_file_route = r'C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv'
            try:
                # Leer el archivo CSV y almacenar las filas
                with open(dollar_file_route, mode='r', newline='') as csv_file:
                    reader_csv = csv.reader(csv_file)
                    rows = list(reader_csv)  # Convertir el contenido a una lista para modificarlo

                # Modificar la primera fila con los nuevos datos
                rows[1] = [current_date, exchange_rate]  # Modifica la fila 1 (índice 0 suele ser el encabezado)

                # Escribir el archivo CSV con las filas actualizadas
                with open(dollar_file_route, mode='w', newline='') as csv_file:
                    writer_csv = csv.writer(csv_file)
                    writer_csv.writerows(rows)  # Sobrescribir el archivo con las filas modificadas
                print("Precio del dólar actualizado con éxito en la base de datos y en el CSV.")
            except FileNotFoundError:  # Si el archivo no ha sido encontrado en la ruta especificada
                print("Archivo no encontrado.")  # Impresión del mensaje de error
        else:  # Si no hay un dato en el campo accedido durante el webscraping
            print("No se pudo encontrar el tipo de cambio en la página.")  # Impresión del mensaje correspondiente
    else:  # Si no se pudo acceder a la página
        print(f"Error al acceder a la página: {response.status_code}")  # Impresión del mensaje correspondiente
"""

def sum_of_settled_amounts(cursor):
    # Consulta correspondiente para la suma de los importes finiquitados
    query = "SELECT SUM(PrecioTotal) FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Comprado'"
    cursor.execute(query)  # Ejecutar la consulta
    result = cursor.fetchone()  # Obtener el resultado de la suma
    print(f"Resultado bruto: {result}")  # Impresión del resultado de la consulta
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado para que muestre el número con dos decimales
    print(f"La suma de los importes es: {formatted_result}\n")  # Imprimir el resultado
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def sum_of_payments_for_lots_to_be_sold(cursor):
    query = "SELECT SUM(CantidadAbonada) FROM Gestion_de_lotes.Abonos"  # Consulta correspondiente
    cursor.execute(query)  # Ejecutar la consulta
    result = cursor.fetchone()  # Obtener el resultado de la suma
    print(f"Resultado bruto: {result}")  # Impresión del resultado de la consulta
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado para que muestre el número con dos decimales
    print(f"La suma de los abonos es: {formatted_result}")  # Imprimir el resultado
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def client_consultation(cursor):
    print("Clientes registrados: \n")  # Impresión informativa
    query = "SELECT IdCliente, Nombre FROM Gestion_de_lotes.Clientes"  # Consulta para imprimir los ID y los nombres
    # de los clientes registrados
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de cada uno de los registros de la tabla
    for row in info:  # Impresión de cada uno de los registros
        print(row)
    while True:  # Bucle infinito que se cicla cada vez que haya una entrada errónea del usuario
        option = input("\nIngrese el ID del cliente cuya información quiera consultar: ")
        if option.isnumeric():  # Si lo que digitó el usuario es un número
            if int(option) < (len(info) + 1):  # Si el número introducido está en el rango del número
                # disponible de registros en la tabla
                # Consulta auxiliar para imprimir los datos del cliente especificado
                auxQuery = f"SELECT * FROM Gestion_de_lotes.Clientes WHERE IdCliente = {option}"
                cursor.execute(auxQuery)  # Ejecución de la consulta auxiliar
                info = cursor.fetchall()  # Obtención del resultado
                for row in info:  # Impresión de los datos
                    print(row)
                break  # Salida del bucle
            else:  # Si el ID no existe en la tabla
                print("El cliente no existe, intente de nuevo.")  # Impresión del mensaje de error correspondiente
        else:  # Si lo que introdujo el usuario no es un número como tal
            print("Opción no válida. Intente de nuevo.")  # Impresión del mensaje correspondiente
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def lot_consultation(cursor):
    lot_number = input("Introduzca el número de lote: ")  # Preguntar por el número de lote
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")  # Manzana del lote
    # Mostrar la información correspondiente
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = " + block_number + " and NoLote = " + lot_number
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de los datos del lote
    for row in info:  # Impresión de los datos del lote
        print(row)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


# Esta función está nada más para hacer ajustes de información en las bases de datos por si se requiere
def info_adjustment(cursor, connection):
    # Ruta del archivo correspondiente
    df = pd.read_csv(r"C:\\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")
    print(df)  # Impresión de los datos en formato bruto para confirmar que los datos se leyeron
    for _, row in df.iterrows():  # Bucle para recorrer cada registro
        # Consulta para insertar los datos en la tabla correspondiente
       sql = """#INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados, CostoMetroCuadrado,
        #PrecioTotal, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
        cursor.execute(sql, tuple(row))  # Ejecución de la consulta
        connection.commit()  # Guardado de los cambios en la base de datos
    subprocess.call("cls", shell=True)


# En este método se eliminó el parámetro del sistema experto por motivos de diseño
def lot_purchase(cursor):
    print("Lista de lotes disponibles:\n")
    # Consulta para obtener la información de los lotes disponibles
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de la información
    columns = cursor.column_names  # Obtención de los nombres de las columnas
    column_width = []  # Generación de un arreglo vacío para almacenar el ancho de columna

    for index, column in enumerate(columns):  # Bucle que recorre cada una de las columnas
        # Obtención de la anchura de cada una de las columnas
        max_width = max(len(str(fila[index])) for fila in info) if info else 0
        column_width.append(max(max_width, len(column)))  # Incluir el tamaño obtenido al arreglo

    for index, column in enumerate(columns):  # Segundo bucle para recorrer las columnas
        print(column.ljust(column_width[index]), end="\t")  # Impresión de las columnas ajustando su tamaño
    print()

    for row in info:  # Bucle para recorrer toda la información recolectada por la consulta previa
        for index, data in enumerate(row):  # Bucle anidado para la impresión de los registros
            print(str(data).ljust(column_width[index]), end="\t")  # Impresión de cada registro con el ajuste de tamaño
        print()
    print("\n¿Cuál lote se quiere comprar?")

    # Después de desplegar los lotes se piden los datos correspondientes
    no_manzana = int(input("Introduzca el número de manzana: "))
    no_lote = int(input("Introduzca el número de lote: "))
    # while True:
    #     client = input("Ingrese el nombre del comprador: ")
    #     proceed = input(f"¿Seguro que este es el nombre del comprador?: {client}\nSí <1>     No <Cualquier tecla>")
    #     if proceed == "1":
    #         break
    # Obtención de los detalles del lote de la base de datos mediante la consulta correspondiente
    query = (f"SELECT MtsCuadrados, CostoMetroCuadrado, PrecioTotal FROM Gestion_de_lotes.Lotes WHERE NoManzana = "
             f"{no_manzana} AND NoLote = {no_lote}")
    cursor.execute(query)  # Ejecución de la consulta
    lot_details = cursor.fetchone()  # Se usa fetchone() ya que se busca un lote en específico
    ################################################
    # if lot_details:  # Si hay detalles en el registro especificado
    #     mts_cuadrados, costo_metro_cuadrado, precio_total = lot_details  # Inicialización de las variables restantes
    #     # para el entrenamiento
    #     recommendation = rule_system.recommend_action(no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado,
    #                                                   precio_total)  # Instancia del sistema experto con cada uno de los
    #     # datos del registro
    #     print("\nRecomendación del sistema experto:")
    #     print(recommendation)  # Dependiendo del precio del dólar se da la recomendación correspondiente
    # else:
    #     # Si el lote que se quiere analizar no se encuentra en la base de datos mostrar el siguiente mensaje
    #     print("Lote no encontrado.")
    ################################################
    proceeding = input("¿Quiere proceder? Sí <1>    No <Cualquier tecla>: ")
    if proceeding == "1":  # Si se quiere proceder después de saber la recomendación
        while True:  # Bucle infinito que repite la solicitud del precio por metro cuadrado en caso de que se ingrese
            # un dato inválido
            try:
                price_per_square_meter = float(input("¿Cuál es el precio por metro cuadrado que se pactó?: "))
                break
            except ValueError:
                print("Ingrese un número válido.")
        aux_query = "SELECT Nombre FROM Gestion_de_lotes.Clientes"  # Consulta auxiliar para obtener los nombres
        # registrados
        cursor.execute(aux_query)  # Ejecución de la consulta auxiliar
        customer_names = list(cursor.fetchall())  # Conversión del conjunto de nombres a una lista de tuplas
        customer_names_formatted = [element[0] for element in customer_names]  # Conversión de la tupla de nombres
        # a una lista
        print("Estos son los clientes registrados: \n")
        print(customer_names_formatted)
        customer_name = input("Ingrese el nombre del cliente: ")  # Ingreso del nombre del cliente
        if customer_name not in customer_names_formatted:  # Si el nombre que se ingresó no está registrado
            print("El cliente no está registrado. ")  # Mensaje de advertencia de que el cliente no está
            # en la base de datos
            address = input("Ingrese su domicilio: ")  # Ingreso del domicilio
            phone_number = input("Ingrese su número de teléfono: ")  # Ingreso del número de teléfono
            # Consulta para insertar los datos del nuevo cliente
            client_insert_query = (f"INSERT INTO Gestion_de_lotes.Clientes (Nombre, Domicilio, Telefono) VALUES "
                                   f"(\'{customer_name}\', \'{address}\', \'{phone_number}\')")
            cursor.execute(client_insert_query)  # Ejecución de la consulta
            conexion.commit()  # Guardado de los cambios
            # Consulta para conseguir el ID del cliente que se registró
            id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \'{customer_name}\'"
            cursor.execute(id_client_query)  # Ejecución de la consulta
            client_id = cursor.fetchone()[0]  # Guardado del ID mediante el uso de un índice
        else:
            # Consulta para conseguir el ID del cliente en la base de datos
            id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \'{customer_name}\'"
            cursor.execute(id_client_query)  # Ejecución de la consulta
            client_id = cursor.fetchone()[0]  # Guardado del ID mediante el uso de un índice
        # Consulta para obtener los metros cuadrados del lote a comprar
        lot_data_query = f"SELECT MtsCuadrados FROM gestion_de_lotes.Lotes WHERE NoManzana = {no_manzana} AND NoLote = {no_lote}"
        cursor.execute(lot_data_query)  # Ejecución de la consulta
        square_meters = cursor.fetchone()[0]  # Obtención del dato usando un índice
        lot_price = price_per_square_meter * float(square_meters)  # Multiplicación del costo por metro cuadrado por los metros
        # cuadrados del lote para obtener el precio total
        print(f"El precio del lote es: ${lot_price} pesos.")  # Importe total del lote
        payment_method = PaymentOptions(conexion)  # Se crea un objeto que contiene los modos de pago
        while True:  # Repetir la impresión del submenú hasta que el usuario decida salir
            try:
                print("Posibles formas de pago:\n")
                print("De contado              <1>")
                print("Anticipo, parcialidades <2>")
                print("En especie              <3>")
                print("Salir     <Cualquier tecla>\n")
                choice = input("Seleccione uno: ")  # Decisión del usuario
                if choice == "1":  # Si se va a pagar de contado se invoca el método correspondiente de la clase
                    payment_method.cash_payment(cursor, no_lote, no_manzana, price_per_square_meter, lot_price, client_id)
                    break
                elif choice == "2":  # Si se va a pagar por abonos se invoca el método correspondiente de la clase
                    payment_method.payment_by_installments(cursor, no_lote, no_manzana, price_per_square_meter, lot_price, client_id)
                    break
                elif choice == "3":  # Si se va a pagar en especie se invoca el método correspondiente de la clase
                    payment_method.payment_in_kind(cursor, no_lote, no_manzana, price_per_square_meter, lot_price, client_id)
                    break
                else:  # Si el usuario quiere salir el bucle se detendrá y regresará al menú principal
                    break
            except ValueError:
                print("Ingrese una opción válida.")
    # # Imprimir los nombres de las columnas
    # print("\t".join(columnas))  # Usamos '\t' para separar por tabulación
    # # Imprimir las filas de la tabla sin paréntesis ni comas
    # for fila in info:
    #     fila_sin_comas = "\t".join(map(str, fila))  # Convertimos a cadena y separamos por tabulación
    #     print(fila_sin_comas)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def balance_consultation(cursor):
    print("---------Consulta de saldo--------")
    # Solicitud de los datos necesarios
    lot_number = input("Introduzca el número de lote: ")
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")
    # Consulta correspondiente
    query = ("SELECT Saldo FROM Gestion_de_lotes.Abonos WHERE NoManzana = " + block_number + " and NoLote = " +
             lot_number + " and NoAbono = (SELECT MAX(NoAbono) FROM Gestion_de_lotes.Abonos WHERE NoManzana = " +
             block_number + " and NoLote = " + lot_number + ")")  # Dentro de esta consulta hay una sub-consulta
    # que obtiene el saldo actual del lote en proceso de compra
    cursor.execute(query)  # Ejecución de la consulta
    balance = cursor.fetchone()  # Se obtiene el dato, es decir, el monto faltante a pagar para liquidar la compra y
    # luego se imprime
    print("El saldo del lote número " + lot_number + " de la manzana " + block_number + " es: $" + balance[0])
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def recording_installment(cursor):
    print("Lotes en proceso de compra")
    payment_method = PaymentOptions(conexion)
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'En proceso de compra'"
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de la información
    columns = cursor.column_names  # Obtención de los nombres de las columnas
    column_width = []  # Generación de un arreglo vacío para almacenar el ancho de columna

    for index, column in enumerate(columns):  # Bucle que recorre cada una de las columnas
        # Obtención de la anchura de cada una de las columnas
        max_width = max(len(str(fila[index])) for fila in info) if info else 0
        column_width.append(max(max_width, len(column)))  # Incluir el tamaño obtenido al arreglo

    for index, column in enumerate(columns):  # Segundo bucle para recorrer las columnas
        print(column.ljust(column_width[index]), end="\t")  # Impresión de las columnas ajustando su tamaño
    print()

    for row in info:  # Bucle para recorrer toda la información recolectada por la consulta previa
        for index, data in enumerate(row):  # Bucle anidado para la impresión de los registros
            print(str(data).ljust(column_width[index]), end="\t")  # Impresión de cada registro con el ajuste de tamaño
        print()
    print("\n¿Cuál lote se quiere abonar?")
    # Después de desplegar los lotes se piden los datos correspondientes
    no_manzana = int(input("Introduzca el número de manzana: "))
    no_lote = int(input("Introduzca el número de lote: "))
    # Consulta para obtener el costo por metro cuadrado y el importe total de lote
    lot_query = f"SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = {no_manzana} AND NoLote = {no_lote}"
    cursor.execute(lot_query)  # Ejecución de la consulta
    lot_data = cursor.fetchall()[0]  # Obtención de la tupla de datos.
    price_per_square_meter = lot_data[4]  # Obtención del precio por metro cuadrado
    lot_price = lot_data[5]  # Obtención del precio total
    # Consulta para obtener el ID del cliente
    client_query = (f"SELECT IdComprador FROM Gestion_de_lotes.Abonos WHERE NoManzana = {no_manzana} "
                    f"AND NoLote = {no_lote}")
    cursor.execute(client_query)  # Ejecución de la consulta
    client_id = cursor.fetchone()[0]  # Obtención del ID del cliente
    # Llamada a la función correspondiente para registrar el abono
    payment_method.payment_by_installments(cursor, no_lote, no_manzana, price_per_square_meter, lot_price, client_id)
    """
#############################################################################################################
#############################################################################################################

########## Funciones nuevas ##########

# Funciones complementarias

def registrar_cliente(cursor):
    print("Registro de nuevo cliente")

    nombre = input("Nombre (puede dejarse en blanco): ").strip()
    domicilio = input("Domicilio (puede dejarse en blanco): ").strip()
    tel_fijo = input("Teléfono fijo (puede dejarse en blanco): ").strip()
    tel_cel = input("Teléfono celular (puede dejarse en blanco): ").strip()

    # Inserta los datos en la tabla, permitiendo valores NULL
    query = """
            INSERT INTO Gestion_de_lotes.Clientes (nombre, domicilio, telefono, celular)
            VALUES (%s, %s, %s, %s) \
            """
    cursor.execute(query, (nombre, domicilio, tel_fijo, tel_cel))
    conexion.commit()
    # Obtener el ID del nuevo cliente
    nuevo_id = cursor.lastrowid
    print(f"Cliente registrado con ID: {nuevo_id}")

def mostrar_datos_cliente(cursor):
    while True:
        # Obtener y mostrar lista de clientes registrados
        cursor.execute("SELECT id, nombre FROM gestion_de_lotes.Clientes")
        clientes = cursor.fetchall()
        # Si no hay clientes en la tabla, mostrar mensaje correspondiente
        if not clientes:
            print("No hay clientes registrados.")
            return
        # Lista de todos los clientes disponibles
        print("\nClientes disponibles:")
        for cliente in clientes:
            print(f"ID: {cliente[0]} - Nombre: {cliente[1]}")
        # Si el valor ingresado por el usuario no está dentro del rango de la lista o es un carácter inválido
        try:
            id_elegido = int(input("\nIngresa el ID del cliente que deseas consultar: "))
        except ValueError:
            print("Entrada inválida. Debes ingresar un número.")
            continue

        # Buscar cliente con el ID ingresado
        cursor.execute("SELECT * FROM gestion_de_lotes.Clientes WHERE id = %s", (id_elegido,))
        resultado = cursor.fetchone()

        if resultado: # Si hay un registro se despliega la información correspondiente
            print("\nDatos del cliente:")
            columnas = [desc[0] for desc in cursor.description]
            for col, val in zip(columnas, resultado):
                print(f"{col}: {val}")
            break  # Salir del bucle si encontró el cliente
        else:
            print("No se encontró ningún cliente con ese ID. Intenta de nuevo.\n")

def modificar_cliente(cursor):
    # Mostrar todos los clientes
    cursor.execute("SELECT id, nombre, domicilio, telefono, celular FROM gestion_de_lotes.Clientes")
    clientes = cursor.fetchall()
    print("Lista de clientes:")
    for cliente in clientes:
        print(f"ID: {cliente[0]}\n Nombre: {cliente[1]}\n Domicilio: {cliente[2]}\n Tel. fijo: {cliente[3]}\n Celular: {cliente[4]}\n")

    try:
        id_seleccionado = int(input("\nIngrese el ID del cliente que desea modificar: "))
        cursor.execute("SELECT nombre, domicilio, telefono, celular FROM gestion_de_lotes.Clientes WHERE id = %s", (id_seleccionado,))
        cliente = cursor.fetchone()

        if cliente:
            print("\nDeje en blanco si no desea cambiar un campo.")

            nuevo_nombre = input(f"Nombre [{cliente[0]}]: ") or cliente[0]
            nuevo_domicilio = input(f"Domicilio [{cliente[1]}]: ") or cliente[1]
            nuevo_fijo = input(f"Teléfono fijo [{cliente[2]}]: ") or cliente[2]
            nuevo_celular = input(f"Celular [{cliente[3]}]: ") or cliente[3]

            cursor.execute("""
                UPDATE gestion_de_lotes.Clientes
                SET nombre = %s, domicilio = %s, telefono = %s, celular = %s
                WHERE id = %s
            """, (nuevo_nombre, nuevo_domicilio, nuevo_fijo, nuevo_celular, id_seleccionado))

            conexion.commit()
            print("\nCliente actualizado correctamente.")
        else:
            print("No se encontró un cliente con ese ID.")

    except ValueError:
        print("Entrada inválida. Debe ingresar un número entero.")


def mostrar_todos_los_datos_de_lotes_vendidos(cursor):
    print("LISTA DE TODOS LOS LOTES VENDIDOS: ")
    cursor.execute("select "
                   "b.nombre, "
                   "a.id_lote, "
                   "a.no_lote, "
                   "a.no_manzana,"
                   "a.col_norte,"
                   "a.col_sur,"
                   "a.col_oriente,"
                   "a.col_poniente,"
                   "a.mts_cuadrados,"
                   "a.costo_por_metro_cuadrado,"
                   "a.precio_total,"
                   "a.estatus,"
                   "a.fecha_contrato,"
                   "a.fecha_pago_final,"
                   "a.restante,"
                   "a.tipo_pago,"
                   "a.comentarios_lotes from gestion_de_lotes.lotes a join gestion_de_lotes.Clientes b "
                   "on a.id_comprador = b.id where a.estatus = 'V'")
    datos_lotes_vendidos = cursor.fetchall()
    if not datos_lotes_vendidos:
        print("No hay lotes vendidos.")
        return
    encabezado_datos_lotes_vendidos = [
        "Nombre comprador", "ID lote", "No. lote", "No. manzana", "Colindancia norte", "Colindancia sur",
        "Colindancia oriente", "Colindancia poniente", "Metros cuadrados", "Costo por metro cuadrado", "Importe total",
        "Estatus", "Fecha de contrato", "Fecha pago final", "Restante", "Tipo de pago", "Comentarios"
    ]
    anchos = [50, 8, 8, 16, 50, 50, 50, 50, 18, 28, 15, 7, 18, 17, 8, 30, 300]
    # Imprimir encabezado
    for i, campo in enumerate(encabezado_datos_lotes_vendidos):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))

    for lotes in datos_lotes_vendidos:
        fila = [
            str(lotes[0]), str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]),
            str(lotes[5]), str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]),
            str(lotes[10]), str(lotes[11]), str(lotes[12]), str(lotes[13]), str(lotes[14]),
            str(lotes[15]), str(lotes[16])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    input("\nPresiona Enter para continuar...")

def mostrar_todos_los_datos_de_lotes_proceso_compra(cursor):
    print("LISTA DE TODOS LOS LOTES EN PROCESO DE COMPRA: ")
    cursor.execute("select "
                   "b.nombre, "
                   "a.id_lote, "
                   "a.no_lote, "
                   "a.no_manzana,"
                   "a.col_norte,"
                   "a.col_sur,"
                   "a.col_oriente,"
                   "a.col_poniente,"
                   "a.mts_cuadrados,"
                   "a.costo_por_metro_cuadrado,"
                   "a.precio_total,"
                   "a.estatus,"
                   "a.fecha_contrato,"
                   "a.fecha_pago_final,"
                   "a.restante,"
                   "a.tipo_pago,"
                   "a.comentarios_lotes from gestion_de_lotes.lotes a join gestion_de_lotes.Clientes b "
                   "on a.id_comprador = b.id where a.estatus = 'P'")
    datos_lotes_proceso_compra = cursor.fetchall()
    if not datos_lotes_proceso_compra:
        print("No hay lotes en proceso de compra.")
        return
    encabezado_datos_lotes_proceso_compra = [
        "Nombre comprador", "ID lote", "No. lote", "No. manzana", "Colindancia norte", "Colindancia sur",
        "Colindancia oriente", "Colindancia poniente", "Metros cuadrados", "Costo por metro cuadrado", "Importe total",
        "Estatus", "Fecha de contrato", "Fecha pago final", "Restante", "Tipo de pago", "Comentarios"
    ]
    anchos = [50, 8, 8, 16, 50, 50, 50, 50, 18, 28, 15, 7, 18, 17, 8, 30, 300]
    # Imprimir encabezado
    for i, campo in enumerate(encabezado_datos_lotes_proceso_compra):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))

    for lotes in datos_lotes_proceso_compra:
        fila = [
            str(lotes[0]), str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]),
            str(lotes[5]), str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]),
            str(lotes[10]), str(lotes[11]), str(lotes[12]), str(lotes[13]), str(lotes[14]),
            str(lotes[15]), str(lotes[16])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    input("\nPresiona Enter para continuar...")

def mostrar_todos_los_datos_de_lotes_disponibles(cursor):
    print("LISTA DE TODOS LOS LOTES DISPONIBLES: ")
    cursor.execute("select "
                   "id_lote, "
                   "no_lote, "
                   "no_manzana,"
                   "col_norte,"
                   "col_sur,"
                   "col_oriente,"
                   "col_poniente,"
                   "mts_cuadrados,"
                   "costo_por_metro_cuadrado,"
                   "precio_total,"
                   "estatus,"
                   "fecha_contrato,"
                   "fecha_pago_final,"
                   "restante,"
                   "tipo_pago,"
                   "comentarios_lotes from gestion_de_lotes.lotes "
                   "where estatus = 'D'")
    datos_lotes_disponibles = cursor.fetchall()
    if not datos_lotes_disponibles:
        print("No hay lotes disponibles.")
        return
    encabezado_datos_lotes_disponibles = [
        "ID lote", "No. lote", "No. manzana", "Colindancia norte", "Colindancia sur",
        "Colindancia oriente", "Colindancia poniente", "Metros cuadrados", "Costo por metro cuadrado", "Importe total",
        "Estatus", "Fecha de contrato", "Fecha pago final", "Restante", "Tipo de pago", "Comentarios"
    ]
    anchos = [8, 8, 16, 50, 50, 50, 50, 18, 28, 15, 7, 18, 17, 8, 30, 300]
    # Imprimir encabezado
    for i, campo in enumerate(encabezado_datos_lotes_disponibles):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))

    for lotes in datos_lotes_disponibles:
        fila = [
            str(lotes[0]), str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]),
            str(lotes[5]), str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]),
            str(lotes[10]), str(lotes[11]), str(lotes[12]), str(lotes[13]), str(lotes[14]),
            str(lotes[15])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()

# Pendiente
def modificar_lote(cursor):
    print("MODIFICAR LOTE")
    no_manzana = input("Ingrese el número de manzana: ").strip()
    no_lote = input("Ingrese el número del lote: ").strip()

    # Buscar el lote con unión a la tabla clientes
    consulta = """
        SELECT l.*, c.nombre AS nombre_comprador
        FROM Lotes l
        LEFT JOIN clientes c ON l.id_comprador = c.id_comprador
        WHERE l.no_manzana = %s AND l.no_lote = %s
    """
    cursor.execute(consulta, (no_manzana, no_lote))
    lote = cursor.fetchone()

    if lote is None:
        print("No se encontró un lote con esos datos.")
        return

    # Mostrar la información del lote verticalmente
    print("\nDatos actuales del lote:")
    for campo, valor in lote.items():
        print(f"{campo}: {valor}")

    if lote["id_comprador"] is None:
        print("\nEste lote no tiene comprador asignado. No se puede modificar.")
        return

    print("\nDeje en blanco los campos que no desea modificar.")

    nuevos_datos = {}

    # Campos modificables
    campos_modificables = [
        "mts_cuadrados",
        "costo_por_metro_cuadrado",
        "fecha_contrato",
        "tipo_pago",
        "comentarios_lotes"
    ]

    for campo in campos_modificables:
        valor = input(f"Ingrese nuevo valor para {campo} (actual: {lote[campo]}): ").strip()
        if valor != "":
            nuevos_datos[campo] = valor

    if not nuevos_datos:
        print("No se ingresaron cambios.")
        return

    # Construir la consulta de actualización
    set_clause = ", ".join([f"{campo} = %s" for campo in nuevos_datos])
    valores = list(nuevos_datos.values()) + [no_manzana, no_lote]

    actualizacion = f"""
        UPDATE Lotes
        SET {set_clause}
        WHERE no_manzana = %s AND no_lote = %s
    """
    cursor.execute(actualizacion, valores)
    print("Lote actualizado correctamente.") # pendiente


def mostrar_detalles_lotes_vendidos(cursor):
    cursor.execute("select count(*) from gestion_de_lotes.lotes where estatus = 'V'")
    no_lotes_vendidos = cursor.fetchone()[0]
    print(f"Número de lotes vendidos: {no_lotes_vendidos}")
    cursor.execute("select sum(precio_total) from gestion_de_lotes.lotes where estatus = 'V'")
    sumatoria_total_lotes_vendidos = cursor.fetchone()[0]
    cantidad = f"$ {sumatoria_total_lotes_vendidos:,.2f} pesos"
    print(f"Suma de los precios totales de los lotes vendidos: {cantidad}")
    cursor.execute("select "
                   "b.nombre, "
                   "a.id_lote, "
                   "a.no_lote, "
                   "a.no_manzana,"
                   "a.mts_cuadrados,"
                   "a.costo_por_metro_cuadrado,"
                   "a.precio_total,"
                   "a.estatus,"
                   "a.fecha_contrato,"
                   "a.fecha_pago_final,"
                   "a.tipo_pago,"
                   "a.comentarios_lotes from gestion_de_lotes.lotes a join gestion_de_lotes.Clientes b "
                   "on a.id_comprador = b.id where a.estatus = 'V'")
    detalles_lotes_vendidos = cursor.fetchall()
    if not detalles_lotes_vendidos:
        print("No hay lotes vendidos.")
        return
    encabezado_lotes = [
        "ID Lote", "No. lote", "No. manzana", "Metros cuadrados", "Costo por metro cuadrado", "Importe total",
        "Estatus", "Fecha de contrato", "Fecha pago final", "Tipo de pago", "Comentarios"
    ]
    # Ajustes de ancho por columna
    anchos = [8, 8, 11, 16, 25, 13, 7, 20, 17, 30, 300]


    for lotes in detalles_lotes_vendidos:
        nombre_comprador = lotes[0]
        print(f"\nNombre del comprador: {nombre_comprador}")
        # Imprimir encabezado
        for i, campo in enumerate(encabezado_lotes):
            print(campo.ljust(anchos[i]), end=' | ')
        print("\n" + "-" * (sum(anchos) + len(anchos) * 3))
        fila = [
            str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]), str(lotes[5]),
            str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]), str(lotes[10]),
            str(lotes[11])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    input("\nPresiona Enter para continuar...")

def mostrar_detalles_lotes_proceso_de_compra(cursor):
    cursor.execute("select count(*) from gestion_de_lotes.Lotes where estatus = 'P'")
    no_lotes_proceso_compra = cursor.fetchone()[0]
    print(f"Número de lotes en proceso de compra: {no_lotes_proceso_compra}")
    cursor.execute("select sum(precio_total) from gestion_de_lotes.lotes where estatus = 'P'")
    sumatoria_total_lotes_en_proceso_compra = cursor.fetchone()[0]
    cantidad = f"$ {sumatoria_total_lotes_en_proceso_compra:,.2f} pesos"
    print(f"Suma de los precios totales de los lotes en proceso de compra: {cantidad}")
    cursor.execute("""select a.id_lote, a.no_lote, a.no_manzana, a.precio_total - b.pagado
                      from gestion_de_lotes.lotes a inner join (select id_comprador, id_lote, sum(cantidad) as pagado
                      from gestion_de_lotes.pagos group by id_comprador, id_lote) b on a.id_comprador = b.id_comprador 
                      and a.id_lote = b.id_lote and a.estatus = 'P'""")
    datos = cursor.fetchall()
    cobranza_pendiente = sum(fila[3] for fila in datos if fila[3] is not None)
    print(f"Cobranza pendiente: $ {cobranza_pendiente:,.2f} pesos")
    suma_abonos_hechos = sumatoria_total_lotes_en_proceso_compra - cobranza_pendiente
    print(f"Suma total de los pagos hechos hasta el momento de estos lotes: $ {suma_abonos_hechos:,.2f} pesos")
    cursor.execute("select "
                   "b.nombre, "
                   "a.id_lote, "
                   "a.no_lote, "
                   "a.no_manzana,"
                   "a.mts_cuadrados,"
                   "a.costo_por_metro_cuadrado,"
                   "a.precio_total,"
                   "a.estatus,"
                   "a.fecha_contrato,"
                   "a.restante,"
                   "a.tipo_pago,"
                   "a.comentarios_lotes from gestion_de_lotes.lotes a join gestion_de_lotes.Clientes b "
                   "on a.id_comprador = b.id where a.estatus = 'P'")
    detalles_lotes_proceso_compra = cursor.fetchall()
    if not detalles_lotes_proceso_compra:
        print("No hay lotes en proceso de compra.")
        return
    encabezado_lotes = [
        "ID Lote", "No. lote", "No. manzana", "Metros cuadrados", "Costo por metro cuadrado", "Importe total",
        "Estatus", "Fecha de contrato", "Saldo restante", "Tipo de pago", "Comentarios"
    ]
    # Ajustes de ancho por columna
    anchos = [8, 8, 11, 16, 25, 13, 7, 20, 20, 30, 300]


    for lotes in detalles_lotes_proceso_compra:
        nombre_comprador = lotes[0]
        print(f"\nNombre del comprador: {nombre_comprador}")
        # Imprimir encabezado
        for i, campo in enumerate(encabezado_lotes):
            print(campo.ljust(anchos[i]), end=' | ')
        print("\n" + "-" * (sum(anchos) + len(anchos) * 3))
        fila = [
            str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]), str(lotes[5]),
            str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]), str(lotes[10]),
            str(lotes[11])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    input("\nPresiona Enter para continuar...")



######################################################################################################

# Funciones base

def operaciones_clientes(cursor):
    while True:  # Bucle infinito para desplegar el submenú de las operaciones sobre los clientes
        print("<1> Registrar un cliente")
        print("<2> Visualizar los datos de un cliente")
        print("<3> Modificar cualquier dato de un cliente")
        print("<Cualquier tecla> Salir")
        eleccion = input("¿Qué es lo que quiere hacer?")
        if eleccion == "1":
            registrar_cliente(cursor)
        elif eleccion == "2":
            mostrar_datos_cliente(cursor)
        elif eleccion == "3":
            modificar_cliente(cursor)
        else:
            break

def consulta_de_saldos_y_ganancias(cursor):
    while True:  # Bucle infinito para desplegar el submenú de las operaciones sobre los clientes
        print("<1> Consultar detalles de los lotes en proceso de compra")
        print("<2> Consultar detalles de los lotes vendidos")
        print("<Cualquier tecla> Salir")
        eleccion = input("¿Qué es lo que quiere hacer?")
        if eleccion == "1":
            mostrar_detalles_lotes_proceso_de_compra(cursor)
        elif eleccion == "2":
            mostrar_detalles_lotes_vendidos(cursor)
        else:
            break

def operaciones_lotes(cursor):
    while True:  # Bucle infinito para desplegar el submenú de las operaciones sobre los clientes
        print("<1> Consultar los datos de los lotes vendidos")
        print("<2> Consultar los datos de los lotes en proceso de compra")
        print("<3> Consultar los datos de los lotes disponibles")
        print("<4> Modificar un dato de un lote")
        print("<Cualquier tecla> Salir")
        eleccion = input("¿Qué es lo que quiere hacer?")
        if eleccion == "1":
            mostrar_todos_los_datos_de_lotes_vendidos(cursor)
        elif eleccion == "2":
            mostrar_todos_los_datos_de_lotes_proceso_compra(cursor)
        elif eleccion == "3":
            mostrar_todos_los_datos_de_lotes_disponibles(cursor)
        elif eleccion == "4":
            modificar_lote(cursor)
        else:
            break
# Pendiente
def registrar_una_venta_o_un_abono(cursor):
    # Obtener y mostrar lista de clientes registrados
    cursor.execute("SELECT id, nombre FROM gestion_de_lotes.Clientes")
    clientes = cursor.fetchall()
    if not clientes:
        print("No hay clientes registrados.")
        return
    encabezado_clientes = ["ID cliente", "Nombre"]
    anchos = [10, 70]
    for i, campo in enumerate(encabezado_clientes):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))
    for lotes in clientes:
        fila = [
            str(lotes[0]), str(lotes[1])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    while True:
        try:
            id_ingresado = input("Ingrese el id del cliente que desea hacer la compra: ")
            if id_ingresado not in clientes:
                print("El cliente no existe. Proceda a registrarlo")
                registrar_cliente(cursor)
                break
        except ValueError:
            print("Ingrese dato válido, por favor.")

    mostrar_todos_los_datos_de_lotes_disponibles(cursor)
    while True:
        try:
            id_lote = input("Ingrese el id del lote que se va a vender: ")
            break
        except ValueError:
            print("Ingrese dato válido, por favor.")



def modificar_pagos_por_lote(cursor):
    # 1. Pedir datos al usuario
    manzana = input("Ingresa el número de manzana: ").strip()
    lote = input("Ingresa el número de lote: ").strip()

    # 2. Buscar id_lote
    cursor.execute("""
                   SELECT id_lote
                   FROM gestion_de_lotes.Lotes
                   WHERE no_manzana = %s
                     AND no_lote = %s
                   """, (manzana, lote))
    resultado = cursor.fetchone()

    if not resultado:
        print("No se encontró ningún lote con esos datos.")
        return
    id_lote = resultado[0]

    # 3. Buscar pagos relacionados y obtener el nombre del comprador
    cursor.execute("""
                   SELECT id_pago,
                          fecha,
                          id_comprador,
                          id_lote,
                          no_abono,
                          cantidad,
                          no_recibo,
                          moneda,
                          tipo_cambio,
                          cantidad_extranjera,
                          comentarios_pagos
                   FROM gestion_de_lotes.Pagos 
                   WHERE id_lote = %s
                   """, (id_lote,))
    pagos = cursor.fetchall()

    if not pagos:
        print("No hay pagos registrados para ese lote.")
        return

    cursor.execute("""SELECT c.nombre 
                      FROM gestion_de_lotes.Clientes c join gestion_de_lotes.Pagos p 
                      ON c.id = p.id_comprador
                      WHERE p.id_lote = %s LIMIT 1""", (id_lote,))
    nombre = cursor.fetchone()[0]

    # 4. Mostrar los pagos como tabla
    print("Nombre del comprador: {}".format(nombre))
    print("\nPagos encontrados:")
    encabezado = [
        "ID Pago", "Fecha", "ID_Comprador", "ID_lote", "Abono", "Cantidad",
        "No. Recibo", "Moneda", "Tipo Cambio",
        "Cant. Extranjera", "Comentarios"
    ]
    # Ajustes de ancho por columna
    anchos = [8, 12, 20, 10, 7, 10, 12, 8, 13, 18, 300]

    # Imprimir encabezado
    for i, campo in enumerate(encabezado):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))

    # Imprimir filas
    for pago in pagos:
        fila = [
            str(pago[0]), str(pago[1]), str(pago[2]), str(pago[3]), str(pago[4]),
            str(pago[5]), str(pago[6]), str(pago[7]), str(pago[8]), str(pago[9]),
            str(pago[10])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()

    # 5. Permitir al usuario elegir un pago a modificar por su ID
    while True:
        id_elegido = input("\nIngresa el ID del pago que deseas modificar (o escribe 'salir' para terminar): ").strip()
        if id_elegido.lower() == 'salir':
            break

        try:
            id_pago = int(id_elegido)
        except ValueError:
            print("ID inválido. Debe ser un número.")
            continue

        # Verificar si el ID ingresado está en la lista de pagos
        pagos_ids = [p[0] for p in pagos]
        if id_pago not in pagos_ids:
            print("Ese ID no está en la lista de pagos mostrados.")
            continue

        # Pedir nuevos valores
        nuevo_recibo = input("Nuevo número de recibo (deja en blanco para no cambiar): ").strip()
        nueva_fecha = input("Nueva fecha (YYYY-MM-DD) (deja en blanco para no cambiar): ").strip()
        nuevos_comentarios = input("Nuevo comentario (deja en blanco para no cambiar): ").strip()

        campos = []
        valores = []

        if nuevo_recibo:
            campos.append("no_recibo = %s")
            valores.append(nuevo_recibo)
        if nueva_fecha:
            campos.append("fecha = %s")
            valores.append(nueva_fecha)
        if nuevos_comentarios:
            campos.append("comentarios_pagos = %s")
            valores.append(nuevos_comentarios)

        if campos:
            sql = f"UPDATE pagos SET {', '.join(campos)} WHERE id_pago = %s"
            valores.append(id_pago)
            cursor.execute(sql, tuple(valores))
            print("Pago actualizado.\n")
        else:
            print("No se realizaron cambios.\n")

def desplegar_pagos_de_un_lote(cursor):
    no_manzana = input("Ingrese el número de manzana: ").strip()
    no_lote = input("Ingrese el número del lote: ").strip()

    cursor.execute(f"""select a.nombre from gestion_de_lotes.Clientes a join gestion_de_lotes.Lotes b 
                      on a.id = b.id_comprador where b.no_lote = {no_lote} and no_manzana = {no_manzana}""")
    nombre_comprador = cursor.fetchone()[0]
    print(f"Nombre del comprador: {nombre_comprador}\n")
    cursor.execute(f"""select b.estatus as estatus_lote, a.id_pago, a.fecha, a.id_comprador, a.id_lote, a.no_abono, a.cantidad, a.no_recibo, 
                             a.tipo_pago, a.moneda, a.tipo_cambio, a.cantidad_extranjera, a.comentarios_pagos
                             from gestion_de_lotes.Pagos a join gestion_de_lotes.Lotes b on a.id_lote = b.id_lote 
                             where b.no_lote = {no_lote} and b.no_manzana = {no_manzana}
    """)
    pagos_rescatados = cursor.fetchall()
    encabezado_pagos_rescatados = [
        "Estatus lote", "ID pago", "Fecha", "ID comprador", "ID lote",
        "No. abono", "Cantidad abonada", "No. recibo", "Tipo de pago", "Moneda",
        "Tipo de cambio", "Cantidad extranjera", "Comentarios pagos"
    ]
    # Ajustes de ancho por columna
    anchos = [12, 7, 15, 13, 8, 9, 17, 10, 50, 6, 15, 20, 300]
    # Imprimir encabezado
    for i, campo in enumerate(encabezado_pagos_rescatados):
        print(campo.ljust(anchos[i]), end=' | ')
    print("\n" + "-" * (sum(anchos) + len(anchos) * 3))
    for lotes in pagos_rescatados:
        fila = [
            str(lotes[0]), str(lotes[1]), str(lotes[2]), str(lotes[3]), str(lotes[4]),
            str(lotes[5]), str(lotes[6]), str(lotes[7]), str(lotes[8]), str(lotes[9]),
            str(lotes[10]), str(lotes[11])
        ]
        for i, celda in enumerate(fila):
            print(celda.ljust(anchos[i]), end=' | ')
        print()
    input("\nPresiona Enter para continuar...")

def menu_principal(cursor):
    # Menú principal en la consola
    while True:  # Bucle infinito que se ejecuta hasta que el usuario quiera salir del programa
        print("Sistema de control de venta de lotes avanzado. Menú principal")
        print("<1> Operaciones sobre clientes")
        print("<2> Hacer una consulta de los saldos y las ganancias")
        print("<3> Operaciones sobre lotes")
        print("<4> Registrar una venta o un abono")
        print("<5> Modificar datos de un pago")
        print("<6> Visualizar los pagos hechos de un lote en proceso de compra")
        print("<Cualquier tecla> Salir")
        eleccion = input("Seleccione la operación que quiera realizar: ")
        if eleccion == "1":  # Si el usuario quiere revisar o modificar algo acerca de los clientes
            operaciones_clientes(cursor)
        elif eleccion == "2":  # Si el usuario quiere consultar información específica de saldos y ganancias
            consulta_de_saldos_y_ganancias(cursor)
        elif eleccion == "3":  # Si el usuario quiere revisar o modificar algo acerca de los lotes registrados
            operaciones_lotes(cursor)
        elif eleccion == "4":  # Si el usuario quiere iniciar con el registro de una venta o iniciar el proceso de una
            registrar_una_venta_o_un_abono(cursor)
        elif eleccion == "5":  # Si el usuario quiere revisar o modificar algo acerca de un pago registrado
            modificar_pagos_por_lote(cursor)
        elif eleccion == "6":
            desplegar_pagos_de_un_lote(cursor)
        else:
            break

    """
    # rule_system = ExpertSystem(float(exchange_rate))  # Instancia del sistema experto
    # # Cada vez que se ejecuta el programa se entrena el sistema experto con los datos dentro del archivo Lotes.csv
    # rule_system.train_model(r"C:\\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")
    while True:  # Bucle infinito que se ejecuta hasta que el usuario quiera salir del programa
        print("\n\nIniciar la compra de lote: (1)")
        print("Consultar un lote: (2)")
        print("Consultar la sumatoria de los importes finiquitados: (3)")
        print("Consultar la sumatoria de los abonos de los lotes en proceso de compra: (4)")
        print("Consultar el saldo de un lote: (5)")
        print("Consultar los datos de un cliente: (6)")
        print("Hacer ajuste de datos (7)")
        print("Chatear con asistente virtual: (8)")  # Opción para llamar al chatbot
        print("Registrar un abono de un lote en proceso de compra: (9)")
        print("Salir (Cualquier tecla)\n")
        eleccion = input("Seleccione la operación que quiera realizar: ")
        if eleccion == "1":  # Si se quiere registrar la compra de un lote se llama a la función "compra de lote"
            lot_purchase(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "2":  # Si se quiere consultar los datos de un lote en específico se llama a la función
            # "Consulta de lote"
            lot_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "3":  # Si se quiere consultar la sumatoria de los montos de los lotes ya comprados se llama
            # a la función "Sumatoria de montos finiquitados"
            sum_of_settled_amounts(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "4":  # Si se quiere consultar la sumatoria de los abonos de los lotes en proceso de compra
            # se llama a la función correspondiente
            sum_of_payments_for_lots_to_be_sold(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "5":  # Si se quiere consultar el saldo de un lote en proceso de compra se llama a la función
            # "Consulta de saldo"
            balance_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "6":  # Si se quieren consultar los datos de un cliente en específico se llama a la función
            # "Consulta de cliente"
            client_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif eleccion == "7":  # Opción para modificar algún dato de algún registro
            # Pendiente
            subprocess.call("cls", shell=True)
        elif eleccion == "8":  # Opción para llamar al chatbot
            assistant = LotSalesAssistant()
            assistant.chat()
            subprocess.call("cls", shell=True)
        elif eleccion == "9":  # Opción para registrar un abono en una compra de un lote por parcialidades
            recording_installment(cursor)
            subprocess.call("cls", shell=True)
        else:
            break
            
    """


def conexion_sql():  # Función para conectar a la base de datos
    # Conectar a la base de datos MySQL
    return mysql.connector.connect(  # Retorno de la conexión a la base de datos correspondiente
        host='localhost',
        database='gestion_de_lotes',
        user='root',
        password='mysql24$^ui(yuAs'
    )


def conseguir_conexion():  # Función para obtener la conexión a la base de datos para el asistente virtual
    global conexion  # Asignación de la conexión como global para que sea accesible en el código principal y se pueda
    # importar en cualquier momento desde alguna clase del proyecto
    if not conexion.is_connected():  # Si la conexión se interrumpió
        conexion = conexion_sql()  # Volver a intentar a conectar a la base de datos
    return conexion  # Retorno de la conexión

#################################################
try:
    conexion = conexion_sql()  # Conexión inicial
    # connection.autocommit = False
except Error as e:  # Si no hubo conexión por alguna razón
    print("(1)Error al conectar a MySQL", e)

if __name__ == "__main__":  # Si este archivo se está ejecutando como el programa principal
    if conexion.is_connected():  # Si la conexión ha sido exitosa
        cursor = conexion.cursor()  # Se crea el cursor necesario para ejecutar consultas
        # ajuste_de_informacion(cursor, connection)
        actualizar_precio_dolar(cursor)  # Llamada a la función que actualiza el precio del dólar en la base de datos
        menu_principal(cursor)  # Llamada a la función que contiene el menú
        conexion.commit()  # Confirmar los cambios en la base de datos
        cursor.close()  # Cierra del cursor
        conexion.close()  # Se cierra la conexión para confirmar el cierre definitivo de la sesión
        print("Conexión a MySQL cerrada")  # Mensaje del cierre de la conexión
