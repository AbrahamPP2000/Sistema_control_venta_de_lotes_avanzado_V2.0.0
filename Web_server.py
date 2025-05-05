# import csv  # Para el manejo de archivos CSV a la hora de importar datos
# import subprocess  # Para limpiar la pantalla después de cada operación.
# import pandas as pd  # Para el formato de la información a la hora de imprimir detalles de la base de datos
# import requests  # Para acceder a la página web Google Finance para obtener el precio del dólar
# from bs4 import BeautifulSoup  # Para la revisión y extracción de información de archivos html y xml de páginas web
# from datetime import datetime  # Para la extracción de la fecha actual del sistema operativo a la hora de actualizar
# # el precio del dólar
# import mysql.connector  # Para la conexión con la base de datos MySQL
# from mysql.connector import Error  # Para lanzar un mensaje de error en caso de no poder acceder a la base de datos
from Payment_Options import PaymentOptions  # Clase del proyecto en donde están las formas posibles de pago
# from Sales_assistant import LotSalesAssistant  # Nueva importación

from flask import Flask, render_template, request, redirect, url_for
from Payment_Options import PaymentOptions
from Data_Import_and_processing import conexion_sql

app = Flask(__name__)
conexion = conexion_sql()
cursor = conexion.cursor()

@app.route('/')
def home():
    return render_template('index.html')



@app.route("/comprar", methods=["GET"])
def mostrar_lotes_disponibles():
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
    cursor.execute(query)
    lotes = cursor.fetchall()
    columnas = cursor.column_names
    return render_template("comprar.html", lotes=lotes, columnas=columnas)


@app.route("/procesar_compra", methods=["POST"])
def procesar_compra():
    manzana = request.form.get("manzana")
    lote = request.form.get("lote")

    # Aquí podrías redirigir a otra página para elegir cliente, forma de pago, etc.
    # O directamente iniciar el flujo de compra desde PaymentOptions

    # Por ejemplo: mostrar un formulario con nombre del cliente y tipo de pago
    return render_template("registro_compra.html", manzana=manzana, lote=lote)


@app.route("/guardar_compra", methods=["POST"])
def guardar_compra():
    manzana = int(request.form.get("manzana"))
    lote = int(request.form.get("lote"))
    cliente = request.form.get("cliente")
    precio = float(request.form.get("precio"))
    forma_pago = request.form.get("forma_pago")

    # Conseguir el ID del cliente, registrarlo si no existe, etc.
    # Calcular el precio del lote (usando los metros cuadrados)
    # Llamar a la lógica de PaymentOptions

    payment = PaymentOptions(conexion)
    client_id = obtener_o_registrar_cliente(cliente)

    cursor.execute(f"SELECT MtsCuadrados FROM gestion_de_lotes.Lotes WHERE NoManzana = {manzana} AND NoLote = {lote}")
    mts = cursor.fetchone()[0]
    total = mts * precio

    if forma_pago == "contado":
        payment.cash_payment(cursor, lote, manzana, precio, total, client_id)
    elif forma_pago == "parcialidades":
        payment.payment_by_installments(cursor, lote, manzana, precio, total, client_id)
    elif forma_pago == "especie":
        # Aquí podrías pedir descripción antes
        payment.payment_in_kind(cursor, lote, manzana, precio, total, client_id)

    return redirect(url_for("mostrar_lotes_disponibles"))


if __name__ == '__main__':
    app.run(debug=True)