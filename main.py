import src.generadorClientes as generadorClientes
import src.utils as utils
import src.Servidor as sv
import threading
import src.Temporizador as tmp


servidores : sv.Servidor = []

def main():
    global servidores
    numUsuarios = int(input("Ingrese el número de usuarios a generar: "))
    clientes = generadorClientes.generar_clientes(numUsuarios)

    for i in range(4):
        servidores.append(sv.Servidor())

    servidores[0].setCliente(clientes[0])
    servidores[1].setCliente(clientes[1])
    servidores[2].setCliente(clientes[2])
    servidores[3].setCliente(clientes[3])

    utils.listarUsuario(clientes, 0)

    print("En servicio")

    utils.listarUsuario(clientes, 3)

    temporizador = tmp.Temporizador()
    temporizador.iniciar()

    try:
        while temporizador.corriendo:
            temporizador.corriendo = pasarBufer(clientes, temporizador.segundos *100)
            if not temporizador.corriendo:
                temporizador.detener()
                break
    except Exception as e:
        print(e)
        temporizador.detener()
        pass

    #print("Servidores: ", servidores)

def pasarBufer(clientes, segundos):
    global servidores

    servidores_filtrados = filter(lambda x: x.cliente, servidores)


    #Obtener menor tiempo de hora de salida de los clientes en servicio
    menorTiempo = min(servidores_filtrados, key=lambda x: x.acomulado)

    if(menorTiempo.acomulado >= segundos):
        return True
    
    #Obtener el clientes con hll menor a menorTiempo.horaSalida y que esten en estado 0
    for i in range(len(clientes)):
        if(clientes[i].hllgada <= menorTiempo.acomulado and clientes[i].estado == 0):
            clientes[i].estado = 1
            clientes[i].tiempoEspera = menorTiempo.acomulado - clientes[i].hllgada
            clientes[i].tiempoEsperaBonificacion = clientes[i].tiempoEspera + clientes[i].bonificacion

    
    menorTiempo.liberarCliente()

    clientesEnBuffer = list(filter(lambda x: x.estado == 2 , clientes))
    if((3 - len(clientesEnBuffer)) > 0):
        lst = sorted(list(filter(lambda x: x.estado == 1, clientes)), key=lambda x: x.tiempoEsperaBonificacion, reverse=True )
        for i in range(len(lst)):
            if(i<= (3 - len(clientesEnBuffer)) and len(list(filter(lambda x: x.estado == 2 , clientes))) < 3):
                lst[i].estado = 2
            else:
                break

    #Pasar clientes de estado 2 a 3 si hay un servidor disponible, debe ser el mayor en tiempoEsperaBonificacion
    clientesEnBuffer = list(filter(lambda x: x.estado == 2 , clientes))
    if(len(clientesEnBuffer) > 0):
        mayorTiempo = max(clientesEnBuffer, key=lambda x: x.tiempoEsperaBonificacion)
        menorTiempo.setCliente(mayorTiempo)
    


    # Pasar de estado 1 a 2 si hay un bufer disponible
    clientesABuffer = list(filter(lambda x: x.estado == 1, clientes))
    if(len(clientesABuffer) > 0):
        mayorTiempoEsperaBonificacion = max(clientesABuffer, key=lambda x: x.tiempoEsperaBonificacion)
        mayorTiempoEsperaBonificacion.estado = 2

    
    clientesEnServicio = list(filter(lambda x: x.estado == 3, clientes))
    clientesEnBuffer = list(filter(lambda x: x.estado == 2, clientes))
    clientesEnLista = list(filter(lambda x: x.estado == 1, clientes))
    clientesEnEspera = list(filter(lambda x: x.estado == 0, clientes))

    #Limpiar la consola
    print("\033[H\033[J")
    print("En espera")
    utils.listarUsuario(clientesEnEspera, 0)
    print('\n')
    print("En lista")
    utils.listarUsuario(clientesEnLista, 1)
    print('\n')
    print("En buffer")
    utils.listarUsuario(clientesEnBuffer, 2)
    print('\n')
    print("En servicio")
    utils.listarUsuario(clientesEnServicio, 3)

    print("Tiempo: ", segundos)

    return len(clientesEnEspera) > 0 or len(clientesEnLista) > 0 or len(clientesEnBuffer) > 0 or len(clientesEnServicio) > 0

main()