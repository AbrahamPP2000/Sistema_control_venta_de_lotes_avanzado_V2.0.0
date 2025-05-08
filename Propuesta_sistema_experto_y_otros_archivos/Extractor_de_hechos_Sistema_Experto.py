import mysql.connector

def obtener_facts(cliente_id, lote_id):
    conn = mysql.connector.connect(user='tu_user', password='tu_pass', host='localhost', database='tu_db')
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT SUM(monto) FROM pagos WHERE cliente_id = %s", (cliente_id,))
    total_pagado = cursor.fetchone()['SUM(monto)']

    cursor.execute("SELECT precio FROM lotes WHERE id = %s", (lote_id,))
    precio = cursor.fetchone()['precio']

    cursor.execute("SELECT COUNT(*) FROM pagos WHERE cliente_id = %s AND estado = 'atrasado'", (cliente_id,))
    atrasos = cursor.fetchone()['COUNT(*)']

    conn.close()

    return {
        "tipo_pago": "contado" if total_pagado >= precio else "abonos",
        "porcentaje_pagado": int((total_pagado / precio) * 100),
        "pagos_atrasados": atrasos
    }
