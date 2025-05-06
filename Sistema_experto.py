class MotorDeReglas:
    def __init__(self, cursor):
        pass

    def verificar_pago(self, pago, saldo_restante):
        if pago.monto > saldo_restante:
            return "El pago excede el saldo restante del lote."

    def recomendar_lote(self, cliente):
        if cliente.es_nuevo and cliente.presupuesto <= 100000:
            return "Recomendar lotes en zona económica."


