import src.cliente as cliente
import random
class Servidor :

    def __init__(self):
        self.tiempos = {
            "Bancario": [240, 580],
            "Transferido": [700,1400],
            "Empresas": [700,2300],
            "Especial": [240,580],
            "Personal": [240,580],
            "Usuarios": [240,580],
            "VIP": [240,580]
        }
        self.acomulado = 0

    def setCliente(self, cliente : cliente.Cliente):
        self.cliente = cliente
        self.cliente.estado = 3
        self.cliente.tiempoServicio = self.calcularTiempoServicio()
        self.cliente.horaLlegada = self.acomulado
        self.cliente.horaSalida = self.cliente.hllgada + self.cliente.tiempoEspera +self.cliente.tiempoServicio
        self.acomulado += self.cliente.horaSalida

    def liberarCliente(self):
        self.cliente.estado = 4
        self.cliente = None


    def calcularTiempoServicio(self):
        return self.randomServicio(self.tiempos[self.cliente.tipo][0], self.tiempos[self.cliente.tipo][1])

    
    def randomServicio(self, inicio: float, fin : float):
        return random.uniform(inicio, fin)