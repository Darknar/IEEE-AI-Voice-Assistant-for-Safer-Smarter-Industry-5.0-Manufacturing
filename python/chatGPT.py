from json_Hilos import ExtraerDatosConfig
from json_Hilos import GuardarConversacion, ActualizarDatos
from json_Hilos import ContarArchivos
from EyS import Prompt
import variablesG
from openai import OpenAI
from datetime import datetime
from cryptography.fernet import Fernet
import re
import os
import time as t
from markdown import Markdown
from io import StringIO

F = Fernet(b'DT_X8i7KU0BBUZJAyoUfmY_mpFqAMKDFR_s1TTBUmuc=')
client = None
assistant = None
thread = None

#! ----------------------------------------------------------------
#! ---------------------- Funciones internas ----------------------
#! ----------------------------------------------------------------

def unmarkElemento(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmarkElemento(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

def unmark(text):
    # Parcheando la clase Markdown para agregar el formato 'plain'
    Markdown.output_formats["plain"] = unmarkElemento
    __md = Markdown(output_format="plain")
    __md.stripTopLevelTags = False

    return __md.convert(text)

def getAPIKey() -> str:
    """Funcion para obtener la API Key de ChatGPT"""
    return F.decrypt(ExtraerDatosConfig()['CHATGPT']['APIKEY_CIF'].encode()).decode()

def ArchivosAsistente() -> list[str]:
    archivos = []
    
    def ArchivosCarpeta(carpeta : dict, url : str) -> None:
        for _, archivo in carpeta.items():
            if archivo['TIPO'] == 'CARPETA':
                if archivo['ARCHIVOS'] != {}:
                    ArchivosCarpeta(archivo['ARCHIVOS'], url + archivo['URL'])
            else:
                archivos.append(url + archivo['URL'])

    for _, carpeta in ExtraerDatosConfig()['CHATGPT']['ARCHIVOS'].items():
        if carpeta['TIPO'] == 'CARPETA':
            ArchivosCarpeta(carpeta['ARCHIVOS'], variablesG.URL + "/" + carpeta['URL'])
        else:
            archivos.append(variablesG.URL + "/" + carpeta['URL'])
                
    return archivos

def ExisteAsistente() -> bool:
    """Funcion para saber si existe el asistente de ChatGPT en la documentacion"""
    return ExtraerDatosConfig()['CHATGPT']['ASISTENTE'] != ""

def ArchivoDatos() -> str:
    archivo = ExtraerDatosConfig()['CHATGPT']['HISTORICO']['URL']                
    return variablesG.URL + "/" + archivo

def LimpiarMensaje(mensaje : str) -> str:
    "Funcion que elimina todas las referencias a archivos del mensaje"
    
    #Elimina todos los caracteres que se encuentran entre "【" y "】"
    mensaje = unmark(re.sub(r'【[^】]*】', '', mensaje))
    
    return mensaje

def ReiniciarAsistente() -> None:
    vectorStoreID = ExtraerDatosConfig()['CHATGPT']['ALMACEN']
    AsistenteID = ExtraerDatosConfig()['CHATGPT']['ASISTENTE']
    
    vector_store_files = client.beta.vector_stores.files.list(
        vector_store_id=vectorStoreID
    )
    for file in vector_store_files.data:
        client.files.delete(file.id)
    
    client.beta.assistants.delete(assistant_id=AsistenteID)
    client.beta.vector_stores.delete(vector_store_id=vectorStoreID)
    
    ActualizarDatos()
    InicializarCHATGPT(reinicio=True)
    
    

#! ----------------------------------------------------------------
#! ---------------------- Funciones visibles ----------------------
#! ----------------------------------------------------------------

#todo ----------------------------------------------------------- Funcion para inicializar y preparar el asistente de trabajo

def InicializarCHATGPT(reinicio = False) -> None:
    """Funcion para inicializar y preparar el asistente de trabajo"""
    global client, assistant, thread
    
    client = OpenAI(
        api_key= getAPIKey() 
    )

    if ExisteAsistente() and not reinicio:

        id_asistente = ExtraerDatosConfig()['CHATGPT']['ASISTENTE']
        assistant = client.beta.assistants.retrieve(assistant_id=id_asistente)
        
        if not (len(ArchivosAsistente()) == ContarArchivos()):
            print("Faltan archivos")
            ReiniciarAsistente()
    
    else:
        assistant = client.beta.assistants.create(
            name="BOT - Local",
            instructions=Prompt(),
            model=ExtraerDatosConfig()['CHATGPT']['MODELO'],
            tools=[{"type": "file_search"}],
        )
        
        vector_store = client.beta.vector_stores.create(
            name=("Archivos" + str(datetime.now().strftime("%Y_%m_%d"))),
            expires_after={        
                "anchor": "last_active_at",
                "days": 5
            },
        )

        file_streams = [open(path, "rb") for path in ArchivosAsistente()]


        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files = file_streams
        )

        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

        if file_batch.status == "completed":
            print("Datos cargados correctamente")
            
        ActualizarDatos(Asistente=assistant.id,Almacen=vector_store.id)
            
    thread = client.beta.threads.create()



#todo ----------------------------------------------------------- Funcion para generar una consulta

def ConsultaChatGPT(mensaje : str) -> str:
    """Funcion generar una consulta a ChatGPT"""
    
    print("Enviando mensaje a ChatGPT...")
    
    try:
        while os.path.getsize(ArchivoDatos()) == 0:
            t.sleep(1)
        
        message_file = client.files.create(
            file=open(ArchivoDatos(), "rb"), 
            purpose="assistants"
        )
        
        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=mensaje,
            attachments= [{ "file_id": message_file.id, "tools": [{ "type": "file_search" }] }]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            GuardarConversacion(messages.dict())
            client.files.delete(message_file.id)
            
            return LimpiarMensaje(messages.data[0].content[0].text.value)
        else:
            print(run.status)
            
        return None
    
    except Exception as e:
            print(e)
            ReiniciarAsistente()
            client.files.delete(message_file.id)
            return ConsultaChatGPT(mensaje)
        

#todo ----------------------------------------------------------- Funciones para conversion de voz

def EsChatGPTActivadoSintesis() -> bool:
    """Funcion para saber si ChatGPT esta activado para texto-voz"""
    datos = ExtraerDatosConfig()
    return datos['CHATGPT']['ACTIVAR_VOZ']

def EsChatGPTActivadoReconocimiento() -> bool:
    """Funcion para saber si ChatGPT esta activado para voz-texto"""
    datos = ExtraerDatosConfig()
    return datos['CHATGPT']['ACTIVAR_RECONOCIMIENTO']

def VozChatGPT(texto : str, URL : str) -> None:
    """Funcion para obtener la respuesta de ChatGPT mediante audio"""
    
    try:
        # Crear cliente de OpenAI
        client = OpenAI(
            api_key=getAPIKey()
        )
        
        # Crear la consulta
        response = client.audio.speech.create(
            model="tts-1",  # Modelo de texto a voz
            voice="onyx",   # Voz del modelo
            input=texto,    # Texto a convertir
        )
        
        # Guardar el archivo de audio
        with open(URL, "wb") as f:
            f.write(response.content)

    except Exception as e:
        print(e)

#* ----------------------------------------------------------------
#* ---------------------- Funciones de prueba ---------------------
#* ----------------------------------------------------------------

if __name__ == '__main__':
    print(ArchivosAsistente())