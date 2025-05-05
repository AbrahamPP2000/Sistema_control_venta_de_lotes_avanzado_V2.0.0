from datetime import datetime  # Librería para obtener la fecha y hora actuales
import inspect  # Librería para implementar una pila de llamadas de funciones


class PaymentOptions:  # Definición de la clase de las modalidades de pago
    def __init__(self, conn):  # Constructor de la clase
        self.connection = conn  # Atributo que guarda la conexión a la base de datos

    def cash_payment(self, cursor, lote, manzana, sqm_price, lot_price, client_id):
        """Función de pago de contado: Solamente se ingresa un pago único"""
        while True:  # Bucle para solicitar el pago las veces que sean necesarias en caso de que no se ingrese una
            # cantidad que liquide la deuda
            # Ingreso de la cantidad de dinero que se pagó
            payment = float(input("¿Cuánto se pagó? Ingrese la cantidad: "))
            if payment < lot_price:  # Si lo que se ingresó no cubre el importe
                print("El pago no es suficiente.")  # Mostrar el mensaje de advertencia
            else:  # Si el pago fue suficiente
                break  # Salir del bucle
        print(f"Cambio: ${payment - lot_price} pesos")  # Cantidad de dinero excedente
        # Llamada a la función que registra la compra y actualiza el estatus del lote correspondiente
        PaymentOptions.purchase_table_row_insertion_and_lot_update(self, cursor, lote, manzana, sqm_price,
                                                                   lot_price, client_id)
        print("Presione enter")
        input()
        # Operación para deshacer los cambios, ya que el rollback extrañamente no funciona
        # rev_query = ("UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = null, PrecioTotal = null, Estatus = "
        #              "'Disponible' where NoManzana = 1 and NoLote = 8;")
        # cursor.execute(rev_query)
        # self.connection.commit()
        print("Operación hecha.")


    def payment_by_installments(self, cursor, lote, manzana, sqm_price, lot_price, client_id):
        """Función de pago de anticipo, parcialidades: Se ingresan los abonos necesarios para pagar el lote"""
        settled_debt = False  # Bandera para indicar si a la hora de ingresar un abono la deuda se liquida o no
        current_date = datetime.now()  # Fecha y hora actuales
        formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
        print(f"Fecha: {formatted_date}\n")  # Impresión de la fecha actual al momento de ingresar un abono
        # Consulta para cerciorarse de que haya al menos un registro del lote correspondiente
        ascertainment_query = (f"SELECT EXISTS (SELECT 1 FROM Gestion_de_lotes.Abonos WHERE NoManzana = {manzana} "
                               f"and NoLote = {lote})")
        cursor.execute(ascertainment_query)  # Ejecución de la consulta de cercioramiento
        result = True if cursor.fetchone()[0] == 1 else False  # Asignación de un valor booleano a una variable
        # dependiendo del resultado de la consulta
        if result:  # Si ya hay un registro del lote correspondiente en la tabla Abonos
            # Consulta del último abono ingresado antes de la inserción del siguiente abono
            last_installment_query = (f"SELECT * FROM Gestion_de_lotes.Abonos WHERE NoManzana = {manzana} and NoLote "
                                      f"= {lote} and NoAbono = (SELECT MAX(NoAbono) FROM Gestion_de_lotes.Abonos WHERE "
                                      f"NoManzana = {manzana} and NoLote = {lote})")
            cursor.execute(last_installment_query)  # Ejecución de la operación
            last_installment_data = cursor.fetchall()[0]  # Obtención de la tupla de datos de la consulta
            print(last_installment_data)
            receipt_number = int(input("Ingrese el número de recibo: "))  # Ingreso del número de recibo
            # Generación del número de abono correspondiente sumando 1 al valor del último número de abono
            installment_number = last_installment_data[3] + 1
            # Ingreso del abono correspondiente
            installment = float(input("Ingrese el abono depositado, asegúrese de que sea el correcto: $"))
            # Cálculo del saldo restante a partir del registro anterior
            remaining_balance = last_installment_data[6] - installment
            if remaining_balance <= 0:  # Si ya se llega a pagar el lote en su totalidad, es decir, si el saldo llega
                # a 0 cuando se ingrese el abono
                print("Este es el último abono que hace falta para liquidar la deuda.")
                settled_debt = True  # Cambio de la bandera a verdadero
            # Inserción del abono a la tabla correspondiente
            installment_insertion_query = (f"INSERT INTO gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, "
                                           f"CantidadAbonada, NoRecibo, Saldo, IdComprador) VALUES (\'{formatted_date}\', "
                                           f"{manzana}, {lote}, {installment_number}, {installment}, {receipt_number},"
                                           f" {remaining_balance}, {client_id})")
            cursor.execute(installment_insertion_query)  # Ejecución de la operación
            self.connection.commit()  # Guardado de los cambios
            if settled_debt:  # Si la deuda ha sido liquidada con el abono ingresado
                # Llamada a la función que registra la compra y actualiza el estatus del lote correspondiente
                PaymentOptions.purchase_table_row_insertion_and_lot_update(self, cursor, lote, manzana,
                                                                           sqm_price, lot_price, client_id)

        else:  # Si no hay ningún registro del lote correspondiente en la tabla Abonos, significa que la compra apenas
            # comienza y se pagará un anticipo
            while True:  # Bucle para pedir el anticipo y el número de recibo en caso de que se ingresen datos inválidos
                try:
                    # Ingreso del pago de anticipo
                    partial_payment = float(input("Ingrese el anticipo que se pagó: $"))
                    balance = lot_price - partial_payment  # Cálculo del saldo restante
                    receipt_number = int(input("Ingrese el número de recibo: "))  # Ingreso del número de recibo
                    # Inserción del anticipo a la tabla "Abonos"
                    insert_query = (f"INSERT INTO gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, "
                                    f"CantidadAbonada, NoRecibo, Saldo, IdComprador) VALUES (\'{formatted_date}\', "
                                    f"{manzana}, {lote}, 1, {partial_payment}, {receipt_number}, {balance}, "
                                    f"{client_id})")
                    cursor.execute(insert_query)  # Ejecución de la consulta
                    self.connection.commit()  # Guardado de los cambios en la base de datos
                    # Operación en donde se edita el registro correspondiente al lote
                    lot_data_update = (f"UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = {sqm_price}, "
                                       f"PrecioTotal = {lot_price}, Estatus = 'En proceso de compra'")
                    cursor.execute(lot_data_update)  # Ejecución de la operación
                    self.connection.commit()  # Guardado de los cambios
                    break  # Salida del bucle en caso de que el anterior código haya funcionado correctamente
                except ValueError:  # Si el usuario ingresó un dato inválido
                    print("Ingrese datos válidos.")  # Mensaje de error correspondiente

    def payment_in_kind(self, cursor, lote, manzana, sqm_price, lot_price, client_id):
        """Función de pago en especie: Se ingresa lo que se intercambió para pagar el lote"""
        # Ingreso de lo que se intercambió para liquidar la deuda
        payment_in_kind_especifications = input("¿Qué fue lo que se intercambió para liquidar la deuda? ")
        # Llamada a la función que registra la compra y actualiza el estatus del lote correspondiente
        PaymentOptions.purchase_table_row_insertion_and_lot_update(self, cursor, lote, manzana, sqm_price,
                                                                   lot_price, client_id,
                                                                   payment_in_kind_especifications)

    def purchase_table_row_insertion_and_lot_update(self, cursor, lote, manzana, sqm_price, lot_price,
                                                    client_id, in_kind_details=None):
        """Se actualizan las tablas Compras y Lotes cada vez que se liquida una deuda"""
        caller = inspect.stack()[1].function  # Creación de una pila de llamadas de funciones para controlar el flujo
        # de la ejecución
        purchase_type = ""  # Generación de una variable que va a almacenar la modalidad de la compra a registrar
        current_date = datetime.now()  # Obtención de la fecha y hora actuales
        formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
        if caller == "cash_payment":  # Si la función que se llamó durante la compra es para un pago de contado
            print("Compra de contado")
            purchase_type = "Contado"
        elif caller == "payment_by_installments":  # Si la función que se llamó para registrar la compra es para
            # anticipo y parcialidades
            print("Compra por anticipo, parcialidades")
            purchase_type = "Anticipo, parcialidades"
        elif caller == "payment_in_kind":  # Si la función que se llamó es para registrar una compra en especie
            print("Pago en especie")
            purchase_type = "En especie"

        # Operación para insertar el registro de compra correspondiente
        purchase_edition_query = (f"INSERT gestion_de_lotes.Compras (NoManzana, NoLote, CostoPorMetroCuadrado, "
                                  f"ImporteTotal, Fecha, IdCliente, FormaDePago, ArticulosPagoEnEspecie) VALUES "
                                  f"({manzana}, {lote}, {sqm_price}, {lot_price}, \'{formatted_date}\', {client_id}, "
                                  f"\'{purchase_type}\', \'{in_kind_details}\')")
        cursor.execute(purchase_edition_query)  # Ejecución de la operación
        self.connection.commit()  # Guardado de los cambios

        # Consulta para actualizar el registro del lote a comprar: se almacena el costo por metro cuadrado que se
        # pactó, el precio total resultante de la multiplicación previa y el cambio del estatus a "comprado"
        lot_edition_query = (f"UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = {sqm_price}, PrecioTotal = "
                             f"{lot_price}, Estatus = 'Comprado' WHERE NoManzana = {manzana} AND NoLote = {lote}")
        cursor.execute(lot_edition_query)  # Ejecución de la consulta
        self.connection.commit()  # Guardado de los cambios
        print("Revisar tabla compras.")
        input()
