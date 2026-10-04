def calcular_aulas(carga_horaria, minutos_hora_aula):
    minutos_totais = carga_horaria * 60

    aulas = minutos_totais / minutos_hora_aula

    return aulas