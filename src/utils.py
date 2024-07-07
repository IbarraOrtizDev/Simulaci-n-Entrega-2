import src.cliente as cliente
import numpy as np
import pandas as pd

def listarUsuario(listX : cliente.Cliente = [], status = 0):
    if len(listX) == 0:
        return
    columns = ['| ID', '| TIPO', '| TELL', '| HLL', '| BONIFICACIÓN',  '| TE', '| TE + Bonificación']

    if(status != 3):
        data = filter(lambda x: x.estado == status, listX)
        data2 = list(map(lambda x: [x.id, x.tipo, x.tiempoLlegada, x.hllgada, x.bonificacion, x.tiempoEspera, x.tiempoEsperaBonificacion], data))
        data2 = np.array(data2)
        df = pd.DataFrame(data2, columns=columns)
        print(df)
        return
    
    
    columnsType = list(set(list(map(lambda x: x.tipo == status, listX))))

    for i in listX:
        print('\n')
        print('TIPO', i.tipo)
        print('HLL', i.hllgada)
        print('TE', i.tiempoEspera)
        print('T. SERVICIO', i.tiempoServicio)
        print('HLL', i.horaSalida)
        print('ID', i.id)
        print('\n')



