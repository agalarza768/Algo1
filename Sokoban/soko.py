def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []

    for fila in range(len(desc)):
        grilla.append([])
        for columna in range(len(desc[fila])):
            grilla[fila].append(desc[fila][columna])
    
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    columnas = len(grilla[0])
    filas = len(grilla)
    return (columnas, filas)

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == "#"
       
def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] in ".+*"

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] in "$*"

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] in "@+"

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in range(len(grilla)):
        for columna in range(len(grilla[fila])):
            if grilla[fila][columna] in '.+':
                return False
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    for fila in range(len(grilla)):
        for columna in range(len(grilla[fila])):
            if hay_jugador(grilla, columna, fila):
                cJugador_x = columna
                cJugador_y = fila

    c1_x = cJugador_x + direccion[0]
    c1_y = cJugador_y + direccion[1]
    c2_x = c1_x + direccion[0]
    c2_y = c1_y + direccion[1]

    if hay_pared(grilla, c1_x, c1_y):
        return grilla
    if hay_caja(grilla, c1_x, c1_y):
        if hay_pared(grilla, c2_x, c2_y) or hay_caja(grilla, c2_x, c2_y):
            return grilla
    
    nueva_grilla = []

    for fila in range(len(grilla)):
        nueva_grilla.append([])
        for columna in range(len(grilla[0])):
            nueva_grilla[fila].append(grilla[fila][columna])

    if hay_objetivo(grilla, cJugador_x, cJugador_y):
        nueva_grilla[cJugador_y][cJugador_x] = '.'
    else:
        nueva_grilla[cJugador_y][cJugador_x] = ' '

    if hay_objetivo(grilla, c1_x, c1_y):
        nueva_grilla[c1_y][c1_x] = '+'
    else:
        nueva_grilla[c1_y][c1_x] = '@'

    if hay_caja(grilla, c1_x, c1_y):
        if hay_objetivo(grilla, c2_x, c2_y):
            nueva_grilla[c2_y][c2_x] = '*'
        else:
            nueva_grilla[c2_y][c2_x] = '$'    
    return nueva_grilla