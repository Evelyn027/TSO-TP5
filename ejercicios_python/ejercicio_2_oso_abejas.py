"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# TODO PARA EL ESTUDIANTE:
# 1. Define los mecanismos de sincronización necesarios:
# - Un cerrojo (Lock) o semáforo binario para exclusión mutua en el tarro.
# - Un semáforo para despertar al oso cuando el tarro esté lleno.
# - Un semáforo para que las abejas esperen si el tarro está lleno o el oso está comiendo.
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # TODO: Sincronizar el acceso al tarro de miel:
        # 1. Esperar a que el tarro esté disponible.
        sem_tarro_disponible.acquire()
        #Condicion de salida limpia si la sim termino mientras se esperaba
        if not simulacion_activa:
            sem_tarro_disponible.release()
            break
        # 2. Entrar en exclusión mutua con el tarro.
        with mutex:
            # 3. Depositar una porción de miel (tarro_miel += 1).
            tarro_miel += 1
            print(f"Abeja {id_abeja} deposito miel. Tarro: {tarro_miel}/{M}")
            # 4. Si tarro_miel == M, avisar/despertar al oso dormido.
            if tarro_miel == M:
                print(f" Tarro lleno! La abeja {id_abeja} despierta al oso...")
                sem_oso.release()
            # 5. Si no está lleno, permitir que otras abejas sigan produciendo.
            else:
                sem_tarro_disponible.release()
        pass

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        # =====================================================================
        # TODO PARA EL ESTUDIANTE:
        # 1. Esperar pasivamente (bloqueado) hasta que una abeja señale que el tarro está lleno:
        sem_oso.acquire()
        print(f"El oso despierta. Comiendo tarro {tarros_comidos + 1} de {max_tarros}...")
        time.sleep(0.5) # Simular el tiempo comiendo
        # 2. Comerse toda la miel (tarro_miel = 0).
        with mutex:
            tarro_miel = 0
            tarros_comidos += 1
            print("El oso termino de comer y vuelve a dormir.")
        # 3. Incrementar tarros_comidos += 1.
        # 4. Avisar a las abejas que el tarro está vacío y disponible (sem_tarro_disponible.release()).
        sem_tarro_disponible.release()
        # =====================================================================
        pass
        time.sleep(0.05)
        break  # Evita bucle infinito si el alumno no implementó el TODO
        
    simulacion_activa = False
    sem_tarro_disponible.release()

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    # TODO: Crear e iniciar los hilos para el oso y las N abejas
    # Crear e iniciar el hilo del oso
    hilo_oso = threading.Thread(target=oso, args=(2,))
    hilo_oso.start()
    
    # Crear e iniciar los hilos de las abejas
    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        # daemon=True permite que los hilos mueran cuando el prog principal termina
        hilo_abeja = threading.Thread(target=abeja, args=(i+1,), daemon=True)
        hilos_abejas.append(hilo_abeja)
        hilo_abeja.start()
        
    # El hilo principal espera que el oso termine su cuota de tarros
    hilo_oso.join()
    
    print("=" * 60)
    print(" Simulación finalizada correctamente.")
    print("=" * 60)
    pass

