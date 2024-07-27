import src.generadorClientes as generadorClientes
import src.utils as utils
import src.Servidor as sv
import src.Temporizador as tmp

servidores : sv.Servidor = []
contador = 0

def main():
    global servidores
    numUsuarios = int(input("Ingrese el número de usuarios a generar: "))
    clientes = generadorClientes.generar_clientes(numUsuarios)

    numServidores = int(input("Ingrese el número de servidores: "))
    nameFile = input("Ingrese el nombre del archivo: ")

    for i in range(numServidores):
        servidores.append(sv.Servidor())
        servidores[i].setCliente(clientes[i])

    utils.listarUsuario(clientes, 0)

    print("En servicio")

    utils.listarUsuario(clientes, 3)

    temporizador = tmp.Temporizador()
    temporizador.iniciar()

    try:
        while temporizador.corriendo:
            temporizador.corriendo = pasarBufer(clientes, temporizador.segundos *100)
            if not temporizador.corriendo:
                utils.listarUsuario(sorted(clientes, key=lambda x: x.conteo), -1)
                utils.saveFileCsv(clientes, nameFile, numServidores)
                temporizador.detener()
                break
    except Exception as e:
        print(e)
        temporizador.detener()
        pass

def pasarBufer(clientes, segundos):
    global servidores
    global contador

    servidores_filtrados = filter(lambda x: x.cliente, servidores)

    #Obtener menor tiempo de hora de salida de los clientes en servicio
    menorTiempo = min(servidores_filtrados, key=lambda x: x.acomulado)

    if(menorTiempo.acomulado >= segundos):
        return True
    
    #Obtener el clientes con hll menor a menorTiempo.horaSalida y que esten en estado 0 y posteriormente pasarlos a estado 1
    for i in range(len(clientes)):
        if(clientes[i].hllgada <= menorTiempo.acomulado and clientes[i].estado == 0):
            clientes[i].estado = 1
            clientes[i].tiempoEspera = menorTiempo.acomulado - clientes[i].hllgada
            clientes[i].tiempoEsperaBonificacion = clientes[i].tiempoEspera + clientes[i].bonificacion

    #Liberar cliente
    menorTiempo.cliente.horaSalidaServicio = segundos #menorTiempo.cliente.horaInicioServicio + menorTiempo.cliente.tiempoServicio
    menorTiempo.liberarCliente()

    #Pasar clientes de estado 1 a 2 si hay un bufer disponible
    fullBuffer(clientes, segundos)

    #Pasar clientes de estado 2 a 3 si hay un servidor disponible, debe ser el mayor en tiempoEsperaBonificacion
    clientesEnBuffer = list(filter(lambda x: x.estado == 2 , clientes))
    if(len(clientesEnBuffer) > 0):
        mayorTiempo = min(clientesEnBuffer, key=lambda x: x.conteo)
        mayorTiempo.horaInicioServicio = segundos
        menorTiempo.setCliente(mayorTiempo)
    
    # Pasar de estado 1 a 2 si hay un bufer disponible
    fullBuffer(clientes, segundos)

    clientesEnServicio = list(filter(lambda x: x.estado == 3, clientes))
    clientesEnBuffer = list(filter(lambda x: x.estado == 2, clientes))
    clientesEnLista = list(filter(lambda x: x.estado == 1, clientes))
    clientesEnEspera = list(filter(lambda x: x.estado == 0, clientes))

    #Limpiar la consola
    # print("\033[H\033[J")
    print("En espera")
    utils.listarUsuario(clientesEnEspera, 0)
    print('\n')
    print("En lista")
    utils.listarUsuario(clientesEnLista, 1)
    print('\n')
    print("En buffer")
    utils.listarUsuario(sorted(clientesEnBuffer,key=lambda x: x.conteo) , 2)
    print('\n')
    print("En servicio")
    utils.listarUsuario(clientesEnServicio, 3)

    #print("\nTiempo: ", segundos)

    return len(clientesEnEspera) > 0 or len(clientesEnLista) > 0 or len(clientesEnBuffer) > 0 or len(clientesEnServicio) > 0

def fullBuffer(clientes, segundos):
    global contador
    global servidores
    numEmpresa = 1 if len(servidores) <= 4 else 2
    while True:
        clientesEnBuffer = list(filter(lambda x: x.estado == 2 , clientes))
        clientesEnServicio = list(filter(lambda x: x.estado == 3, clientes))
        lst = list(filter(lambda x: x.estado == 1, clientes))

        #Si el cliente con más tiempo de espera en la cola es “Especial”, y si hay un cliente especial en el buffer o siendo atendido, éste no podrá pasar al búffer. Es decir, entre los clientes que hay en el búffer y en las cajas, solo puede haber máximo un cliente de tipo “Especial”.
        if((len(list(filter(lambda x: x.tipo == 'Especial', clientesEnBuffer))) + len(list(filter(lambda x: x.tipo == 'Especial', clientesEnServicio)))) > 0):
            lst = list(filter(lambda x: x.tipo != 'Especial', lst))

        # En el sistema (búffer y cajas), solo se podrá tener un máximo de 1 cliente de tipo “Trasnferido”.
        if((len(list(filter(lambda x: x.tipo == 'Transferido', clientesEnBuffer))) + len(list(filter(lambda x: x.tipo == 'Transferido', clientesEnServicio)))) > 0):
            lst = list(filter(lambda x: x.tipo != 'Transferido', lst))


        # Si un cliente es de tipo “Empresas”, se evalúa la cantidad de cajas disponibles (# de "servidores”, si es mayor a cuatro, se puede tener máximo dos clientes de este tipo en el sistema (búffer y cajas), de lo contrario, se podrá tener máximo un cliente en el sistema.
        if((len(list(filter(lambda x: x.tipo == 'Empresas', clientesEnBuffer))) + len(list(filter(lambda x: x.tipo == 'Empresas', clientesEnServicio)))) >= numEmpresa):
            lst = list(filter(lambda x: x.tipo != 'Empresas', lst))
        

        if(len(clientesEnBuffer) < 3 and len(lst) > 0):
            lst = sorted(lst, key=lambda x: x.tiempoEsperaBonificacion, reverse=True )
            lst[0].estado = 2
            lst[0].conteo = contador
            lst[0].horaLlegadaBuffer = segundos
            contador += 1
        else:
            break

main()