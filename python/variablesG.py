from threading import Event
import os


EventoVoz = Event() 
"""Evento para activar el reconocimiento de voz"""

EventoHablar = Event() 
"""Evento para activar el reconocimiento de voz"""

EventoOPCUA = Event() 
"""Evento para activar la lectura de datos"""

global_local = 0 
"""Variable para saber si se está en modo local o global"""

DatosLeidos = {} 
"""Diccionario para almacenar los datos leídos"""

Var = True
"""Variable para saber si el programa está encendido o apagado"""

Interfaz = None
"""Variable para almacenar la interfaz"""

URL = os.path.dirname(os.path.abspath(__file__)).replace("\\","/") + '/src' 
"""URL de la carpeta src"""