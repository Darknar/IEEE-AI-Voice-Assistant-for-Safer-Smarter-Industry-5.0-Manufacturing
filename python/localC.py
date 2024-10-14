from opcua import Client
from opcua.ua.uaerrors import BadNodeIdUnknown
from json_Hilos import ExtraerDatosConfig
import variablesG

valores = {}
"""Diccionario para almacenar los valores de las variables del cliente OPCUA"""

CLIENTE = None
"""Variable para almacenar el cliente OPCUA"""

#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

def DatosClienteOPCUA() -> str:
    """Función para extraer los datos de la configuración del cliente OPCUA"""
    
    datos = ExtraerDatosConfig()
    
    ip = datos['LOCAL']["IP_PLC"]
    port = datos['LOCAL']["PORT"]
    
    url = f"opc.tcp://{ip}:{port}"
        
    return url

def ExtraerVariablesNombre() -> dict[str]:
    """Función para extraer las variables del cliente OPCUA"""
    
    datos = ExtraerDatosConfig()
    return datos['LOCAL']['VARIABLES']

def CC_OPCUA():
    """Función para conectar el cliente OPCUA al servidor"""
    
    try:
        CLIENTE.connect()
        print("Cliente Conectado")
    except:
        print("Error al Conectar Cliente")
    
def DC_ClienteOPCUA():
    """Función para desconectar el cliente OPCUA del servidor"""
    
    CLIENTE.disconnect()
    print("Cliente Desconectado")
    
    
#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------
    
def GenerarDatos():
    """Función para generar los datos del cliente OPCUA"""
    global CLIENTE ; CLIENTE = Client(DatosClienteOPCUA())
    
    try:
        CC_OPCUA()
        while variablesG.Var:
            variables = ExtraerVariablesNombre()
            
            for _ , iv in variables.items():
                for jc, jv in iv.items():
                    for kc, kv in jv.items():
                        if type(kv) == dict:
                            for lc, lv in kv.items():
                                if type(lv) == dict:
                                    for varc, varv in lv.items():
                                        if type(varv) == dict:
                                            for mc, mv in varv.items():
                                                id = f'ns={jc};s="{kc}"."{lc}"[{varc}]."{mc}"'
                                                valores[mv] = CLIENTE.get_node(id).get_value()
                                        else:
                                            id = f'ns={jc};s="{kc}"."{lc}"[{varc}]'
                                            valores[varv] = CLIENTE.get_node(id).get_value()
                                else:
                                    id = f'ns={jc};s="{kc}"."{lc}"'
                                    valores[lv] = CLIENTE.get_node(id).get_value()
                        else:
                            id = f'ns={jc};s="{kc}"'
                            valores[kv] = CLIENTE.get_node(id).get_value()
        
    except BadNodeIdUnknown:
        print(f"El nodo al que se intenta acceder no existe ->{id}<-")
    finally:
        DC_ClienteOPCUA()

def ExtraerVariables():
    """Función para extraer los datos generados por el cliente OPCUA"""
    return valores

#* ----------------------------------------------------------------
#* ---------------------- Funciones de prueba ---------------------
#* ----------------------------------------------------------------
    
if __name__ == "__main__":
    DC_ClienteOPCUA()