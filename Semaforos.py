import threading
import time
import random

# Semáforo para controlar el acceso exclusivo a la impresora 
# (solo una solicitud a la vez puede imprimir).
impresora_disponible = threading.Semaphore(1)

# Semáforo para controlar la llegada de nuevas solicitudes de impresión.
# Este semáforo actúa como una señal para notificar que hay una nueva solicitud en la cola.
nueva_solicitud = threading.Semaphore(0)

# Lista que actúa como una cola para almacenar solicitudes de impresión pendientes.
cola_impresiones = []

def procesar_impresion(id_solicitud):
    """
    Función que simula el tiempo de procesamiento de la impresora.
    """
    print(f"Procesando impresión de la solicitud {id_solicitud}...")
    # Simulación del tiempo que tarda en procesar la impresión (1 a 3 segundos)
    time.sleep(random.uniform(1, 3))
    print(f"Solicitud {id_solicitud} impresa.")

def imprimir():
    """
    Función ejecutada por el hilo de la impresora que gestiona las solicitudes en la cola.
    Espera una nueva solicitud y luego la imprime en orden de llegada.
    """
    while True:
        # Espera hasta que una nueva solicitud de impresión esté disponible en la cola.
        nueva_solicitud.acquire()

        # Controla el acceso exclusivo a la impresora para que solo una solicitud sea procesada a la vez.
        impresora_disponible.acquire()
        
        # Si hay solicitudes en la cola, las procesa en orden de llegada (FIFO).
        if cola_impresiones:
            solicitud = cola_impresiones.pop(0)  # Sacar la solicitud de la cola
            procesar_impresion(solicitud)        # Procesar la solicitud

        # Libera el semáforo de la impresora para que otra solicitud pueda ser procesada.
        impresora_disponible.release()

def solicitud_impresion(id_solicitud):
    """
    Función que simula la llegada de una nueva solicitud de impresión.
    Agrega la solicitud a la cola y avisa que hay una nueva solicitud lista para imprimir.
    """
    # Agrega la solicitud a la cola de impresiones.
    cola_impresiones.append(id_solicitud)
    print(f"Nueva solicitud de impresión recibida: {id_solicitud}")

    # Libera el semáforo para notificar que ha llegado una nueva solicitud.
    nueva_solicitud.release()

# Crear y lanzar el hilo de la impresora.
# Este hilo se ejecuta de forma continua, procesando cada solicitud en orden.
hilo_impresora = threading.Thread(target=imprimir)
hilo_impresora.start()

# Simulación de la llegada de solicitudes de impresión.
# Cada solicitud es manejada en su propio hilo para simular concurrencia.
for i in range(5):
    time.sleep(random.uniform(0.5, 2))  # Simula el tiempo de espera entre solicitudes
    hilo_solicitud = threading.Thread(target=solicitud_impresion, args=(i+1,))
    hilo_solicitud.start()
