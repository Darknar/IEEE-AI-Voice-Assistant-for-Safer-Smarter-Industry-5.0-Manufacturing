import json
import paho.mqtt.client as mqtt_client
from json_Hilos import ExtraerDatosConfig
from threading import Thread
import random
import variablesG

valores = {}
"""Diccionario para almacenar los valores de MQTT"""

DECODE_PAYLOAD = True      
"""Enable / disable payload"""

#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

def ConectarMQTT():
    """Función para conectar con el broker de MQTT y obtener los datos"""
    
    def ExtraerDatos():
        """Función para extraer los datos de la configuración de MQTT y generar el ID del cliente aleatorio"""
        datos = ExtraerDatosConfig()
        datos["GLOBAL"]["CLIENT_ID"] = f'python-mqtt-{random.randint(0, 1000)}'
        
        return datos["GLOBAL"]
        
    def Conectar(client, userdata, flags, rc): # Revisar puede conectarse muchas veces
        """Función para conectar con el broker de MQTT"""
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    datos = ExtraerDatos()
    client = mqtt_client.Client(client_id=datos["CLIENT_ID"])

    client.on_connect = Conectar
    client.connect(datos["BROKER"], datos["PORT"])
    
    return client

def Suscribir(client, variables):
    """Función para suscribirse a los tópicos de MQTT y obtener los datos"""            
    
    def Mensaje(client, userdata, message):
        """Función para obtener los mensajes de MQTT"""
        
        global DECODE_PAYLOAD
        _data = "" ; nombre = "" ; datos = ""

        if DECODE_PAYLOAD:
            try:
                # Parsear el payload directamente sin usar mqtt_spb_wrapper
                _data = json.loads(message.payload.decode())
                nombre = _data["metrics"][0]["name"]
                datos = _data["metrics"][0]["value"]
            except:
                pass
        
        valores[nombre] = datos
        
        # Comprobar si variableG.Var es False
        if not variablesG.Var:
            # Si es False, desconectar el cliente
            client.disconnect()
    
    for topic in variables:
        client.subscribe(topic)
        client.on_message = Mensaje
    
    return client

def ExtraerTopics() -> dict:
    Topics = {}
    
    for key1, value1 in ExtraerDatosConfig()["GLOBAL"]["VARIABLES"].items():
        if type(value1) == dict:
            for key2, value2 in value1.items():
                if type(value2) == dict:
                    for key3, value3 in value2.items():
                        if type(value3) == dict:
                            for key4, value4 in value3.items():
                                if type(value4) == dict:
                                    for key5, value5 in value4.items():
                                        if type(value5) == dict:
                                            for key6, value6 in value5.items():
                                                Topics[key1 + '/' + key2 + '/' + key3 + '/' + key4 + '/' + key5 + '/' + key6] = value6
                                        else:
                                            Topics[key1 + '/' + key2 + '/' + key3 + '/' + key4 + '/' + key5] = value5
                                else:
                                    Topics[key1 + '/' + key2 + '/' + key3 + '/' + key4] = value4
                        else:
                            Topics[key1 + '/' + key2 + '/' + key3] = value3
                else:
                    Topics[key1 + '/' + key2] = value2
        else:
            Topics[key1] = value1
    
    return Topics

#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------

def GenerarDatos():
    """Función para generar datos a partir de MQTT y almacenarlos en un diccionario"""
    
    try:
        client = ConectarMQTT()
        client = Suscribir(client, ExtraerTopics())
        
        client.loop_forever()        
    finally:
        if client.is_connected():  # Comprobar si el cliente está conectado antes de desconectar
            client.disconnect()
            print("Cliente desconectado")

def ExtraerVariables():
    """Función para extraer las variables generadas por MQTT"""
    return valores

#* ----------------------------------------------------------------
#* ---------------------- Funciones de prueba ---------------------
#* ----------------------------------------------------------------
    
if __name__ == "__main__":
    GenerarDatos()