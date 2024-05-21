from scipy.optimize import fsolve
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt

def graficar_oferta_demanda(ecuacion_demanda, ecuacion_oferta, punto_equilibrio, filename):
    # Convertir las ecuaciones a funciones lambda
    demanda = lambda x: eval(ecuacion_demanda)
    oferta = lambda x: eval(ecuacion_oferta)
    precio_equilibrio = oferta(punto_equilibrio)

    # Crear un rango de valores para x
    x = np.linspace(0, 25, 100)

    # Calcular los valores de demanda y oferta para el rango de x
    y_demanda = demanda(x)
    y_oferta = oferta(x)

    # Graficar las curvas de oferta y demanda
    plt.figure(figsize=(8, 6))
    plt.plot(x, y_demanda, label='Demanda: ' + ecuacion_demanda)
    plt.plot(x, y_oferta, label='Oferta: ' + ecuacion_oferta)

    # Marcar el punto de equilibrio y el área del superávit
    plt.scatter(punto_equilibrio, demanda(punto_equilibrio), color='red', label='Punto de Equilibrio')
    plt.fill_between(x, y_demanda, y_oferta, where=(x <= punto_equilibrio), color='green', alpha=0.3, label='Superávit del Consumidor')

    # Etiquetas y leyenda
    plt.xlabel('Cantidad')
    plt.ylabel('Precio')
    plt.title('Curvas de Oferta y Demanda')
    plt.axhline(y=precio_equilibrio, color='black', linestyle='--', label='Precio de Equilibrio')
    plt.legend()
    plt.grid(True)
    
    # Guardar la gráfica como una imagen
    plt.savefig(filename)
    plt.close()

def calcular_punto_equilibrio(ecuacion_demanda, ecuacion_oferta):
    # Convertir las ecuaciones a funciones lambda
    demanda = lambda x: eval(ecuacion_demanda)
    oferta = lambda x: eval(ecuacion_oferta)

    # Resolver la ecuación de equilibrio D = O
    punto_equilibrio = fsolve(lambda x: demanda(x) - oferta(x), 0)
    
    return punto_equilibrio[0] if len(punto_equilibrio) > 0 else None


def calcular_superavit(punto_equilibrio, ecuacion_demanda, ecuacion_oferta):
    # Convertir las ecuaciones a funciones lambda
    oferta = lambda x: eval(ecuacion_oferta)

    # Calcular precio de equilibrio
    precio_equilibrio = oferta(punto_equilibrio)
    
    demanda = lambda x: eval(ecuacion_demanda) 

    # Calcular superávit
    if demanda(punto_equilibrio) >= precio_equilibrio:
        ecuacion = lambda x: eval(f"{ecuacion_demanda} - {precio_equilibrio}")
        superavit, err = integrate.quad(ecuacion, 0, punto_equilibrio)
    else: 
        superavit = 0

    return superavit

def superavit(ecu_demand, ecu_offer, filename):
    equal_point = calcular_punto_equilibrio(ecu_demand, ecu_offer)
    superavit = calcular_superavit(equal_point, ecu_demand, ecu_offer)
    graficar_oferta_demanda(ecu_demand, ecu_offer, equal_point, filename)
    return superavit
