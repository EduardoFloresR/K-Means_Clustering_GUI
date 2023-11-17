import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def formatear_coordenadas(lista_arrays):
    # Verificar si la lista está vacía
    if not lista_arrays:
        return "[]"

    # Crear la cadena formateada [(x1,y1), (x2,y2), ..., (xn,yn)]
    cadena_formateada = "[" + ", ".join([f"({x},{y})" for x, y in lista_arrays]) + "]"

    return cadena_formateada

def distancia_media_cuadratica(a, b):
    return np.sum((a - b) ** 2)

def k_medias(X, K, centroides_iniciales):
    centroides = np.array(centroides_iniciales, dtype=float)
    
    for _ in range(100):  # Establece un número máximo de iteraciones
        asignaciones = []
        
        # Asigna cada punto al centroide más cercano
        for punto in X:
            distancias = [distancia_media_cuadratica(punto, c) for c in centroides]
            asignaciones.append(np.argmin(distancias))
        
        # Actualiza los centroides sin utilizar np.mean
        for i in range(K):
            puntos_asignados = [X[j] for j in range(len(X)) if asignaciones[j] == i]
            if len(puntos_asignados) > 0:
                # Calcula la media de las coordenadas manualmente
                sum_x, sum_y = 0.0, 0.0
                for punto_asignado in puntos_asignados:
                    sum_x += punto_asignado[0]
                    sum_y += punto_asignado[1]
                centroides[i] = (sum_x / len(puntos_asignados), sum_y / len(puntos_asignados))
    
    return asignaciones, centroides

def ejecutar_k_medias(K, centroides_iniciales):
    # Cerrar la ventana de la gráfica previa, si está abierta
    plt.close('all')

    # Vectores de entrada
    X = np.array([(0.0, -2.0), (-2.0, 1.0), (3.0, 4.0), (-3.0, 5.0), (4.0, -5.0), (-3.0, -2.0), (7.0, 2.0)], dtype=float)

    # Ejecutar el algoritmo k-medias
    asignaciones, centroides_finales = k_medias(X, K, centroides_iniciales)

    # Mostrar resultados en la GUI
    resultado_texto.set("\nResultados finales:")
    for i in range(K):
        resultado_texto.set(resultado_texto.get() + f"\n\nCentroide {i+1}: {tuple(round(coord, 4) for coord in centroides_finales[i])}\n")
        elementos_asignados = [X[j] for j in range(len(X)) if asignaciones[j] == i]
        asigandos = formatear_coordenadas(elementos_asignados)
        resultado_texto.set(resultado_texto.get() + f"Elementos asignados: {asigandos}\n")

    # Graficar clusters
    graficar_clusters(X, asignaciones, centroides_finales)


def graficar_clusters(X, asignaciones, centroides_finales):
    colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    for i in range(len(X)):
        plt.scatter(X[i][0], X[i][1], c=colores[asignaciones[i]], marker='o')

    for i in range(len(centroides_finales)):
        plt.scatter(centroides_finales[i][0], centroides_finales[i][1], c=colores[i], marker='x', s=200, label=f'Centroide {i+1}')

    plt.title('Clusters obtenidos con k-medias')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.grid(True)
    plt.legend()
    plt.show()

def ejecutar_k_medias(K, centroides_iniciales):
    # Cerrar la ventana de la gráfica previa, si está abierta
    plt.close('all')

    # Vectores de entrada
    X = np.array([(0.0, -2.0), (-2.0, 1.0), (3.0, 4.0), (-3.0, 5.0), (4.0, -5.0), (-3.0, -2.0), (7.0, 2.0)], dtype=float)

    # Ejecutar el algoritmo k-medias
    asignaciones, centroides_finales = k_medias(X, K, centroides_iniciales)

    # Mostrar resultados en la GUI
    resultado_texto.set("\nResultados finales:")
    for i in range(K):
        resultado_texto.set(resultado_texto.get() + f"\n\nCentroide {i+1}: {tuple(round(coord, 4) for coord in centroides_finales[i])}\n")
        elementos_asignados = [X[j] for j in range(len(X)) if asignaciones[j] == i]
        asigandos = formatear_coordenadas(elementos_asignados)
        resultado_texto.set(resultado_texto.get() + f"Elementos asignados: {asigandos}\n")

    # Graficar clusters
    graficar_clusters(X, asignaciones, centroides_finales)

def limpiar_datos():
    entry_k.delete(0, tk.END)
    entry_centroides.delete(0, tk.END)
    resultado_texto.set("")
    plt.close('all')  # Cierra todas las ventanas de gráficos abiertas

# Crear la interfaz gráfica
root = tk.Tk()
root.title("K-Medias GUI")

# Etiqueta y entrada para K
label_k = ttk.Label(root, text="Valor de K:")
label_k.grid(row=0, column=0, padx=5, pady=5, sticky="E")
entry_k = ttk.Entry(root)
entry_k.grid(row=0, column=1, padx=5, pady=5, sticky="W")

# Etiqueta y entrada para centroides iniciales
label_centroides = ttk.Label(root, text="Centroides iniciales (separados por ';', coordenadas separadas por ','):")
label_centroides.grid(row=1, column=0, padx=5, pady=5, sticky="E")
entry_centroides = ttk.Entry(root)
entry_centroides.grid(row=1, column=1, padx=5, pady=5, sticky="W")

# Botón para iniciar el agrupamiento
btn_agrupar = ttk.Button(root, text="Iniciar Agrupamiento", command=lambda: ejecutar_k_medias(int(entry_k.get()), [tuple(map(int, punto.split(','))) for punto in entry_centroides.get().split(';')]))
btn_agrupar.grid(row=2, columnspan=2, pady=10)

# Botón para limpiar datos
btn_limpiar = ttk.Button(root, text="Limpiar Datos", command=limpiar_datos)
btn_limpiar.grid(row=3, columnspan=2, pady=10)

# Etiqueta para mostrar resultados
resultado_texto = tk.StringVar()
label_resultado = ttk.Label(root, textvariable=resultado_texto, justify="left")
label_resultado.grid(row=4, columnspan=2, padx=10, pady=10)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
