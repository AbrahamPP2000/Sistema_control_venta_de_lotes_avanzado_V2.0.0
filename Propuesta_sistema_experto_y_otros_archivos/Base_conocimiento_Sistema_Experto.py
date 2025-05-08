rules = []

def regla_descuento_pago_total(facts):
    if facts['tipo_pago'] == 'contado' and facts['porcentaje_pagado'] == 100:
        return "aplicar_descuento"
rules.append(regla_descuento_pago_total)

def regla_cliente_riesgo(facts):
    if facts['pagos_atrasados'] >= 3:
        return "marcar_como_riesgo"
rules.append(regla_cliente_riesgo)
