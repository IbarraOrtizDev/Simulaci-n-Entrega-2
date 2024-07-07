class Cliente:
    def __init__(self, id, tipo, bonificacion, tiempoLlegada, hllgada):
        self.id = id
        self.tipo = tipo
        self.bonificacion = bonificacion
        self.tiempoLlegada = tiempoLlegada
        self.hllgada = hllgada + tiempoLlegada
        self.estado = 0
        self.horaLlegada = 0
        self.horaSalida = 0
        self.tiempoEspera = 0
        self.tiempoEsperaBonificacion = 0
        self.tiempoServicio = 0

    # getters

    def getHllgada(self):
        return self.hllgada
    
    def getAll(self):
        return "ID: " + str(self.id) + " Tipo: " + self.tipo  + " TELL: " + str(self.tiempoLlegada) + " HLL : " + str(self.hllgada)+ " Bonificacion: " + str(self.bonificacion)
    

    
    # setters
    def setId(self, id):
        self.id = id

    def setTipo(self, tipo):
        self.tipo = tipo

    def setBonificacion(self, bonificacion):
        self.bonificacion = bonificacion

    def setTiempoLlegada(self, tiempoLlegada):
        self.tiempoLlegada = tiempoLlegada

    def setHllgada(self, hllgada):
        self.hllgada = hllgada