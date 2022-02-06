from pila import Pila
class EstadosGuardados:
    def __init__(self):
        """Representa una pila de estados del juego"""
        self.estados = Pila()

    def guardar(self, estado):
        """Guarda el estado recibido"""
        self.estados.apilar(estado)

    def deshacer(self):
        """Saca el ultimo estado recibido"""
        return self.estados.desapilar()
    
    def inicio(self):
        """Devuelve True si no hay estados guardados, False en caso contrario"""
        return self.estados.esta_vacia()