import time
import threading

class Temporizador:
    def __init__(self):
        self.segundos = 0
        self.corriendo = False
        self.hilo = None

    def iniciar(self):
        if not self.corriendo:
            self.corriendo = True
            self.hilo = threading.Thread(target=self.cuenta_adelante)
            self.hilo.start()

    def detener(self):
        self.corriendo = False
        if self.hilo is not None:
            self.hilo.join()

    def cuenta_adelante(self):
        while self.corriendo:
            mins, secs = divmod(self.segundos, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(self.tiempo_transcurrido(), end="\r")

            time.sleep(1)
            self.segundos += 1
        print("\n¡Temporizador detenido!")
    
    def tiempo_transcurrido(self):
        horas = self.segundos // 3600
        minutos = (self.segundos % 3600) // 60
        segundos = self.segundos % 60
        return str(horas)+":"+str(minutos)+":"+str(segundos)