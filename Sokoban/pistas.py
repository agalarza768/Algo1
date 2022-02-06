import soko

def buscar_solucion(estado_inicial):
    """Recibe un estado del juego y la utiliza, junto a un diccionario, como argumentos de la funcion backtrack"""
    visitados = {}
    return backtrack(estado_inicial, visitados)

def backtrack(estado, visitados):
    """Si encuentra una solucion, devuelve True y una lista de acciones"""
    visitados[h(estado)] = True
    if soko.juego_ganado(estado):
        return True, []
    for accion in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nuevo_estado = soko.mover(estado, accion)
        if h(nuevo_estado) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solucion_encontrada:
            acciones.insert(0, accion)
            return True, acciones
    return False, None

def h(estado):
    """Transforma ka lista de listas recibida en una tupla de tuplas"""
    for i in range(len(estado)):
        estado[i] = tuple(estado[i])
    estado = tuple(estado)
    return estado