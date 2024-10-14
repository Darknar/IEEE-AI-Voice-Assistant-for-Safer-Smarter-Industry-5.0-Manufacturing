from threading import Event
from threading import Thread
from json_Hilos import ExtraerDatosConfig, GuardarEnArchivo
import variablesG
import time as t
from localC import ExtraerVariables as ExtraerVariablesLocal
from globalC import ExtraerVariables as ExtraerVariablesGlobal
from localC import GenerarDatos as GenerarVariablesLocal
from globalC import GenerarDatos as GenerarVariablesGlobal

#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

def sleep_interruptible(seconds):
    end_time = t.time() + seconds
    while t.time() < end_time:
        if not variablesG.Var:
            break
        t.sleep(0.1)  # duerme en segmentos de 0.1 segundos
        
def Guardar(valores: dict) -> None:
    """Funcion para guardar los datos en la variable global DatosLeidos"""
    
    variablesG.EventoOPCUA.wait()
    variablesG.EventoOPCUA.clear()
    
    variablesG.DatosLeidos = valores
    
    variablesG.EventoOPCUA.set()
    
    GuardarEnArchivo(valores)

def GuardarDatos() -> None:
    """Funcion para guardar los datos cada 5 segundos desde un hilo"""
    print("Guardando datos cada 5 segundos - activado")
    
    while variablesG.Var:
        if(variablesG.global_local  == 1):
            Guardar(ExtraerVariablesLocal())
        
        if(variablesG.global_local  == 2):
            Guardar(ExtraerVariablesGlobal())
            
        sleep_interruptible(5)
        
    print("Guardando datos cada 5 segundos - desactivado")
        
def GenerarDatos() -> None:
    """Funcion para generar los datos dependiendo del modo seleccionado"""
    if(variablesG.global_local == 1):
        GenerarVariablesLocal()
    
    if(variablesG.global_local == 2):
        GenerarVariablesGlobal()
        
def Leer() -> dict:
    """Funcion para leer los datos guardados en la variable global DatosLeidos"""
    variablesG.EventoOPCUA.wait()
    return variablesG.DatosLeidos

def AsignarModo() -> None:
    """Funcion para asignar el modo de lectura de datos"""
    
    datos = ExtraerDatosConfig()
    GL = 0
    
    if (datos['LOCAL']['ESTADO']):
        GL += 1
    
    if (datos['GLOBAL']['ESTADO']):
        GL += 2
        
    if (GL == 3):
        raise Exception("No se puede inicializar ambos modos")
    
    variablesG.global_local = GL
    
#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------
    
def Inicializar() -> None:
    """Funcion para inicializar el sistema de lectura de datos y creación de hilos"""
    
    AsignarModo()
    Thread(target=GenerarDatos).start()    
    Thread(target=GuardarDatos).start()
    

def Prompt() -> str:
    """Funcion para obtener el prompt de ChatGPT"""
    datos = ExtraerDatosConfig()
    lista = ['', 'LOCAL', 'GLOBAL']
    
    return datos['CHATGPT']['PROMPT'] + datos[lista[variablesG.global_local]]['PROMPT']

#* ----------------------------------------------------------------
#* ---------------------- Funciones de prueba ---------------------
#* ----------------------------------------------------------------
    
if __name__ == "__main__":
    AsignarModo()
    print(Prompt())