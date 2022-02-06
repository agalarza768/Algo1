import gamelib

def juego_crear():
    """Inicializar el estado del juego"""

    turno = 0
    grilla = []

    for fila in range(0, 10):
        grilla.append([])
        for columna in range(0, 10):
            grilla[fila].append(' ')
    
    return [grilla, turno]

def juego_actualizar(juego, x, y):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    grilla = juego[0]
    if y < 30 or y >= 330 or x >= 300:
        return juego
    if grilla[(y//30)-1][x//30] == ' ':
        if juego[1] % 2 == 0:
            grilla[(y//30)-1][x//30] = 'O'
        else:
            grilla[(y//30)-1][x//30] = 'X'
        juego[1] += 1
    return juego

def juego_mostrar(juego):
    """Actualizar la ventana"""
    grilla = juego[0]
    gamelib.draw_text('5 en línea', 150, 15)
    for fila in range(len(grilla)):
        for columna in range(len(grilla[0])):
            gamelib.draw_rectangle(columna*30, 30+fila*30, columna*30+30, 30+fila*30+30, outline='white', fill='black')
            if grilla[fila][columna] == 'O':
                gamelib.draw_text('O', 9+columna*30, 37+fila*30, fill='white', anchor='nw')
            if grilla[fila][columna] == 'X':
                gamelib.draw_text('X', 9+columna*30, 37+fila*30, fill='white', anchor='nw')
    if juego[1] % 2 == 0:
        gamelib.draw_text('Turno de O', 10, 340, fill='white', anchor='nw')
    else:
        gamelib.draw_text('Turno de X', 10, 340, fill='white', anchor='nw')


def main():
    juego = juego_crear()

    # Ajustar el tamaño de la ventana
    gamelib.resize(300, 360)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego = juego_actualizar(juego, x, y)
            
gamelib.init(main)