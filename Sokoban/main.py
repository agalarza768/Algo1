import soko
import gamelib
from deshacer import EstadosGuardados
from pistas import buscar_solucion

OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)

CELDA = 64

def nivel_leer(archivo_niveles):
    """Lee el nivel correspondiente y lo devuelve como cadena"""
    nivel = ''
    linea_max = 0
    for linea in archivo_niveles:
        if linea == '\n' and nivel != '':
            break
        if 'Level' in linea or 'from' in linea or '#' not in linea:
            continue
        nivel += linea
        if len(linea) > linea_max:
            linea_max = len(linea) - 1

    nivel = (nivel.strip('\n')).split('\n')
    return nivel, linea_max

def nivel_rellenar_lineas(desc):
    """Rellena las lineas del nivel con espacios vacios para emparejarlas y las devuelve en una lista de cadenas"""
    nivel, linea_max = desc

    for fila in range(len(nivel)):
        if len(nivel[fila]) < linea_max:
            nivel[fila] += ' '*(linea_max - len(nivel[fila]))        
    return nivel

def juego_comandos(ruta_archivo_comandos):
    """Devuelve un diccionario con los comandos como clave y sus respectivas teclas como valor"""
    teclas_de_comandos = {}
    with open(ruta_archivo_comandos, 'r') as archivo_controles:
        for linea in archivo_controles:
            if linea == '\n':
                continue
            comandos = (linea.rstrip('\n')).split(' = ')
            if len(comandos) < 2:
                raise IndexError('El archivo de comandos esta escrito incorrectamente')
            tecla_comando = comandos[0]
            comando = comandos[1]
            teclas_de_comandos[comando] = teclas_de_comandos.get(comando, [])
            teclas_de_comandos[comando].append(tecla_comando)

    return teclas_de_comandos

def juego_mostrar(juego):
    """Actualizar la ventana"""
    for fila in range(len(juego)):
        for columna in range(len(juego[0])):
            gamelib.draw_image('img/ground.gif', columna*CELDA, fila*CELDA)            
            if not soko.hay_pared(juego, columna, fila) and not soko.hay_objetivo(juego, columna, fila) and not soko.hay_caja(juego, columna, fila) and not soko.hay_jugador(juego, columna, fila):
                gamelib.draw_image('img/ground.gif', columna * CELDA, fila * CELDA)
            if soko.hay_pared(juego, columna, fila):
                gamelib.draw_image('img/wall.gif', columna * CELDA, fila * CELDA)
            if soko.hay_caja(juego, columna, fila):
                gamelib.draw_image('img/box.gif', columna * CELDA, fila * CELDA)
            if soko.hay_jugador(juego, columna, fila):
                gamelib.draw_image('img/player.gif', columna * CELDA, fila * CELDA)
            if soko.hay_objetivo(juego, columna, fila):
                gamelib.draw_image('img/goal.gif', columna * CELDA, fila * CELDA)

def main():
    # Inicializar el estado del juego
    juego_iniciado = False

    diccionario_de_comandos = juego_comandos('teclas.txt')

    with open('niveles.txt', 'r') as archivo_niveles: 
        while gamelib.is_alive():
            if juego_iniciado == False or soko.juego_ganado(juego):

                # Crea la instancia para guardar estados
                estados_guardados = EstadosGuardados()

                desc = nivel_leer(archivo_niveles)
                desc_arreglado = nivel_rellenar_lineas(desc)
                juego = soko.crear_grilla(desc_arreglado)
                estado_inicial = juego
                gamelib.resize(len(juego[0])*CELDA, len(juego)*CELDA)
                juego_iniciado = True
                
                #NUEVO
                solucion_encontrada = False

            # Guarda el estado anterior al movimiento
            estado_anterior = juego

            gamelib.draw_begin()
            # Dibujar la pantalla
            juego_mostrar(juego)
            gamelib.draw_end()
        
    
            ev = gamelib.wait(gamelib.EventType.KeyPress)
            if not ev:
                break
            
            
            tecla = ev.key
            # Actualizar el estado del juego, según la `tecla` presionada
            try:
                if tecla in diccionario_de_comandos['NORTE']:
                    juego = soko.mover(juego, NORTE)
                if tecla in diccionario_de_comandos['OESTE']:
                    juego = soko.mover(juego, OESTE)
                if tecla in diccionario_de_comandos['SUR']:
                    juego = soko.mover(juego, SUR)
                if tecla in diccionario_de_comandos['ESTE']:
                    juego = soko.mover(juego, ESTE)
                if tecla in diccionario_de_comandos['REINICIAR']:
                    # Vacia la instancia
                    estados_guardados = EstadosGuardados()
                    juego = estado_inicial
                    continue                        
                if tecla in diccionario_de_comandos['SALIR']:
                    break

                #NUEVO
                if tecla in diccionario_de_comandos['DESHACER']:
                    if estados_guardados.inicio() == True:
                        juego = estado_inicial
                    else:
                        juego = estados_guardados.deshacer()
                    solucion_encontrada = False
                    continue
                if tecla in diccionario_de_comandos['PISTAS']:
                    if not solucion_encontrada:
                        solucion_encontrada, acciones = buscar_solucion(juego)
                    else:
                        juego = soko.mover(juego, acciones.pop(0))

                if juego == estado_anterior:
                    continue
                    
                # Guarda el nuevo estado de juego
                estados_guardados.guardar(estado_anterior)
                
                if not tecla in diccionario_de_comandos['PISTAS']:
                    solucion_encontrada = False
            except:
                raise ValueError('Teclas y/o comandos asignados incorrectamente')
gamelib.init(main)