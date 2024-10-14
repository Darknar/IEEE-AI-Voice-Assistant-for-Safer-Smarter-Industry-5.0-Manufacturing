import speech_recognition as sr
from json_Hilos import ExtraerPalabraAct
from chatGPT import EsChatGPTActivadoReconocimiento as EsChatGPTActivado
from difflib import SequenceMatcher as SM
from threading import Thread
import variablesG

#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

    #? ----------------------------------------------------------------
    #? --------- SpeechRecognition - Reconocimiento de voz ------------
    #? ----------------------------------------------------------------

def EsActivacion(texto, nombre_activacion):
    """Función para verificar si el nombre de activación está en el texto con un margen de error"""
    # Se comprueba si el nombre de activación está en el texto con un margen de error
    for palabra in texto.split():
        if SM(None, palabra.lower(), nombre_activacion.lower()).ratio() >= 0.6:
            return palabra
    return None


def reconocer(recognizer, audio, na : str):
    """Función para reconocer el audio y ejecutar comandos"""
    
    try:
        # Reconoce el audio
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Has dicho: {texto}")
        
        # Verifica si el nombre de activación está en el texto
        var = EsActivacion(texto, na)
        if var != "" and var != None:            
            #borramos el nombre de activación y todo lo que haya antes
            texto = texto[texto.find(var): ]
            texto = texto.replace(var, "")
            
            if texto != "" and texto != None:
                from main import procesarMensaje_fuera            
                print("Activación detectada, ¿qué necesitas?", texto)
                procesarMensaje_fuera(texto)
            else:
                print("Activación detectada, pero no se ha detectado ninguna orden")
                        
    except sr.UnknownValueError:
        print("No te he entendido")
    except sr.RequestError as e:
        print(f"Error de servicio; {e}")


def Escuchar(na : str):
    """Función para escuchar y procesar el audio, este proceso se realiza en un hilo aparte"""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 2000
    
    with sr.Microphone() as source:
        variablesG.EventoVoz.wait()
        
        print("Di algo ...")
        audio = recognizer.listen(source)
        print("Procesando ...")
        Thread(target=reconocer, args=(recognizer, audio, na)).start()
        
def ReconocimientoVozSR():
    """Función para reconocer la voz y ejecutar comandos"""
    print("Reconocimiento de voz activado", ExtraerPalabraAct())
    
    # Bucle principal para escuchar constantemente
    while variablesG.Var:
        try:
            Escuchar(ExtraerPalabraAct())
        except OSError as e:
            if e.errno in [-9999, -9988]:
                print("Error de PyAudio, deteniendo el reconocimiento de voz.")
                with sr.Microphone() as source:
                    microfonos = source.list_microphone_names()
    
                if len(microfonos) == 0:
                    print("No hay micrófonos conectados")
                else:
                    for i, microfono in enumerate(microfonos):
                        print(f"{i}. {microfono}")
                break
            else:
                raise e
    
    print("Reconocimiento de voz desactivado")
        
    #? ----------------------------------------------------------------
    #? -------------- ChatGPT - Reconocimiento de voz -----------------
    #? ----------------------------------------------------------------
        
def ReconocimientoVozCHATGPT():
    """Funcion para reconocer la voz segun el modelo whisper de chatGPT"""
    ...    
    
def ReconocimientoVoz():
    """Función para convertir la voz en texto segun el modelo seleccionado"""
    global app_controller
    
    if (False):
        ReconocimientoVozCHATGPT()
    else:
        ReconocimientoVozSR()
        
#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------

def IniciarReconocimiento():
    """Función para iniciar el reconocimiento de voz"""
    Thread(target=ReconocimientoVoz).start()