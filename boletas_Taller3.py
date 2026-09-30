#Nombre: VentaBoletas
#Autores: Thomas Herrera Parra - Andrés Felipe Muñoz
#Descripción: Simula la venta concurrente de boletas de un concierto, sin lock (con sobreventa) y con lock (correcta).
#Curso: Infraestructuras Paralelas y Distribuidas

import threading, time

boletas = 100                 # recurso compartido
lock = threading.Lock()

def comprar_sin_lock(intentos, resultados, indice):
    global boletas
    vendidas = 0
    for _ in range(intentos):
        if boletas > 0:              # 1) verifica
            time.sleep(0.0005)       # simula consulta a la base de datos
            boletas -= 1             # 2) descuenta
            vendidas += 1
    resultados[indice] = vendidas

def comprar_con_lock(intentos, resultados, indice):
    global boletas
    vendidas = 0
    for _ in range(intentos):
        with lock:                   # sección crítica: verificar + descontar
            if boletas > 0:
                time.sleep(0.0005)
                boletas -= 1
                vendidas += 1
    resultados[indice] = vendidas

def ejecutar(funcion, compradores=10, intentos=20):
    global boletas
    boletas = 100
    resultados = [0] * compradores
    hilos = []
    for i in range(compradores):
        h = threading.Thread(target=funcion, args=(intentos, resultados, i))
        hilos.append(h)
        h.start()
    for h in hilos:
        h.join()
    return sum(resultados), boletas

# Ejemplo de uso
vendidas, restantes = ejecutar(comprar_sin_lock)
print(f"SIN LOCK -> vendidas: {vendidas}, boletas restantes: {restantes}")

vendidas, restantes = ejecutar(comprar_con_lock)
print(f"CON LOCK -> vendidas: {vendidas}, boletas restantes: {restantes}")