from Base_conocimiento_Sistema_Experto import rules

def inferir(facts):
    conclusiones = []
    for regla in rules:
        resultado = regla(facts)
        if resultado:
            conclusiones.append(resultado)
    return conclusiones
