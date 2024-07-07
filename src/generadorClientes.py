import random
import math

import src.cliente as cliente
tiempos = [
    40.801,142.825,39.022,28.786,33.915,40.921,98.281,28.337,16.750,16.307,10.879,44.526,31.845,28.168,49.834,79.578,80.973,1.268,190.481,9.660,1.795,2.443,35.631,115.783,33.727,28.240,15.534,44.893,83.585,38.233,133.174,42.238,41.841,17.919,6.735,28.433,26.745,58.652,41.701,41.183,46.758,84.666,133.706,47.656,13.009,31.240,35.132,91.393,59.545,15.811,12.267,20.176,0.978,16.214,51.155,22.179,13.169,1.631,7.569,10.396,24.221,40.943,43.534,29.357,116.467,17.789,4.716,4.404,77.387,24.180,55.992,51.833,33.017,12.837,41.250,45.940,112.162,37.870,45.653,65.430,20.088,72.752,34.498,35.742,100.226,56.821,15.650,126.837,12.043,100.343,59.009,24.937,21.470,72.737,22.103,29.391,38.928,16.469,37.257,21.160,8.923,36.134,85.875,108.705,88.013,24.845,59.684,86.133,6.000,4.743,0.648,62.086,19.613,82.023,70.183,6.127,10.175,51.842,45.453,65.046,68.637,44.904,43.512,107.509,94.252,76.688,40.404,138.370,6.947,119.882,0.935,3.889,11.260,60.081,49.189,13.471,59.370,12.879,3.280,12.699,29.039,21.552,13.084,13.269,3.710,11.370,38.680,51.975,51.256,44.940,0.027,107.488,8.470,18.279,41.660,9.877,97.511,10.079,62.497,29.676,192.198,16.869,72.130,111.469,8.832,2.045,48.863,4.612,79.681,25.111,106.516,8.354,104.084,52.330,15.078,129.017,77.975,40.510,277.120,117.618,10.389,28.224,95.028,56.133,49.943,44.818,38.755,2.171,8.018,329.457,4.858,2.378,37.859,12.123,44.458,12.879,79.545,64.854,74.933,138.976
]

def tiempoPromedio(lista):
    suma = 0
    for i in range(len(lista)):
        suma = suma + lista[i]
    return suma/len(lista)

def generar_clientes(total_clientes):
    usuariosPorCaja = tiempoPromedio(tiempos)
    distribucion = {
        "Bancario": 0.52,
        "Transferido": 0.01,
        "Empresas": 0.03,
        "Especial": 0.02,
        "Personal": 0.23,
        "Usuarios": 0.17,
        "VIP": 0.02
    }

    bonificacion = {
        "Bancario": 400,
        "Transferido": 0,
        "Empresas": 400,
        "Especial": 1000,
        "Personal": 1000,
        "Usuarios": 0,
        "VIP": 1800
    }
    
    clientesType = []

    for i in range(total_clientes):
        varRnd = random.random()

        if varRnd < distribucion["Bancario"]:
            clientesType.append("Bancario")
        elif varRnd < (distribucion["Bancario"] + distribucion["Transferido"]):
            clientesType.append("Transferido")
        elif varRnd < (distribucion["Bancario"] + distribucion["Transferido"] + distribucion["Empresas"]):
            clientesType.append("Empresas")
        elif varRnd < (distribucion["Bancario"] + distribucion["Transferido"] + distribucion["Empresas"] + distribucion["Especial"]):
            clientesType.append("Especial")
        elif varRnd < (distribucion["Bancario"] + distribucion["Transferido"] + distribucion["Empresas"] + distribucion["Especial"] + distribucion["Personal"]):
            clientesType.append("Personal")
        elif varRnd < (distribucion["Bancario"] + distribucion["Transferido"] + distribucion["Empresas"] + distribucion["Especial"] + distribucion["Personal"] + distribucion["Usuarios"]):
            clientesType.append("Usuarios")
        else:
            clientesType.append("VIP")

    clientes: cliente.Cliente = []

    for i, client in enumerate(clientesType):
        ultimoCliente = clientes[-1] if len(clientes) > 0 else None
        ultimoClienteTiempoLlegada = ultimoCliente.getHllgada() if ultimoCliente is not None else 0
        clientes.append(cliente.Cliente(i+1, 
                                        client, 
                                        bonificacion[client], 
                                        (1/ (-1/usuariosPorCaja) * (math.log(random.random()))),
                                        ultimoClienteTiempoLlegada
                                        )
                        )

    return clientes


# total_clientes = 100
# lista_clientes = generar_clientes(total_clientes)
# for i in lista_clientes:
#     print(i.getAll())