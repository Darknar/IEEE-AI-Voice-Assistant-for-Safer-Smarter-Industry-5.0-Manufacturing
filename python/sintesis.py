from gtts import gTTS
from playsound import playsound
from chatGPT import VozChatGPT
from chatGPT import EsChatGPTActivadoSintesis as EsChatGPTActivado
import variablesG
import os


#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

def eliminarArchivo(archivo_a_eliminar : str) -> None:
    """Función para eliminar un archivo si existe"""
    # Verificar si el archivo existe antes de eliminarlo
    if os.path.exists(archivo_a_eliminar):
        # Eliminar el archivo
        os.remove(archivo_a_eliminar)
    else:
        print("El archivo no existe.")
    
    #? ----------------------------------------------------------------
    #? ----------- GTTS (Google Text to Speech) - Síntesis ------------
    #? ----------------------------------------------------------------     

def TextaVozGTTS(mitexto, lenguaje = 'es' ,Archivo = "audio.mp3") -> None:
    """Función para convertir texto a voz con GTTS"""
    tts = gTTS(text=mitexto, lang=lenguaje)
    # save the audio file
    
    variablesG.EventoHablar.wait()
    variablesG.EventoHablar.clear()
    
    tts.save(variablesG.URL + "/"+ Archivo)
    playsound(variablesG.URL + "/"+ Archivo)
    eliminarArchivo(variablesG.URL + "/"+ Archivo)
    
    variablesG.EventoHablar.set()
    
    #? ----------------------------------------------------------------
    #? -------------- ChatGPT - Síntesis de texto a voz ---------------
    #? ----------------------------------------------------------------
    
def TextaVozChatGPT(mitexto, Archivo = "audio.mp3") -> None:
    """Función para convertir texto a voz con ChatGPT"""
    
    variablesG.EventoHablar.wait()
    variablesG.EventoHablar.clear()
    
    VozChatGPT(mitexto, variablesG.URL + "/"+ Archivo)
    playsound(variablesG.URL + "/"+ Archivo)
    eliminarArchivo(variablesG.URL + "/"+ Archivo)
    
    variablesG.EventoHablar.set()
    
#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------

def TextaVoz(mitexto, Archivo="audio.mp3") -> None:
    """Función para convertir texto a voz con GTTS o ChatGPT dependiendo de la configuración"""
    if (EsChatGPTActivado()):
        TextaVozChatGPT(mitexto, Archivo=Archivo)
    else:
        TextaVozGTTS(mitexto, Archivo=Archivo)
    
#* ----------------------------------------------------------------
#* ---------------------- Funciones de prueba ---------------------
#* ----------------------------------------------------------------

if __name__ == "__main__":
    TextaVoz("Hola, soy tu asistente virtual, ¿en qué puedo ayudarte?")
