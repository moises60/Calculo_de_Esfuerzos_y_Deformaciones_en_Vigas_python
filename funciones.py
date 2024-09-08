import pygame
import matplotlib.pyplot as plt
import numpy as np

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

# Materiales comunes
materiales = {
    'acero': 210e9,
    'madera': 11e9,
    'aluminio': 69e9
}

def calcular_inercia(seccion):
    """
    Argumentos:
    seccion (str): Sección de la viga (rectangular o circular)
    
    Descripción:
    Calcula el momento de inercia de la viga según la sección transversal
    Devuelve el momento de inercia
    """
    if seccion == 'rectangular':
        base = 0.2 
        altura = 0.3 
        return (base * altura**3) / 12
    elif seccion == 'circular':
        radio = 0.15 
        return (np.pi * radio**4) / 4


def dibujar_viga(pantalla, longitud, posicion, carga, seleccion_material, seccion, elastic_modulus, font,materiales_rects,seccion_rects):
    """
    Argumentos:
    pantalla (pygame.Surface): La superficie de pygame donde se dibuja la viga
    longitud (float): Longitud de la viga en metros
    posicion (float): Posición de la carga en metros
    carga (float): Magnitud de la carga en Newtons
    seleccion_material (str): Material seleccionado (acero, madera, aluminio)
    seccion (str): Sección transversal de la vig
    elastic_modulus (float): Módulo de elasticidad del material
    font (pygame.font.Font): Fuente de texto para mostrar información

    Descripción:
    Dibuja la viga, la carga aplicada y muestra información relevante en la pantall
    """
    
    pantalla.fill(WHITE)
    #Si no no pongo esta función aquí no se muestra en pantalla. Originalmente estaba en el main.py pero no se veía 
    dibujar_seleccion_cajas(pantalla, materiales_rects, seccion_rects, seleccion_material, seccion, font)
    pygame.draw.rect(pantalla, GRAY, (100, pantalla.get_height()//2 - 20, longitud * 50, 20))
    
    # Dibujar la carga
    pygame.draw.line(pantalla, BLUE, (100 + posicion * 50, pantalla.get_height()//2 - 50), (100 + posicion * 50, pantalla.get_height()//2), 5)
    pygame.draw.polygon(pantalla, BLUE, [(100 + posicion * 50, pantalla.get_height()//2 - 60), (95 + posicion * 50, pantalla.get_height()//2 - 50), (105 + posicion * 50, pantalla.get_height()//2 - 50)])
    
    texto_longitud = font.render(f'Longitud: {longitud:.1f} m', True, BLACK)
    pantalla.blit(texto_longitud, (50, 50))
    
    texto_carga = font.render(f'Carga: {carga} N', True, BLACK)
    pantalla.blit(texto_carga, (50, 100))
    
    texto_posicion = font.render(f'Posición de la carga: {posicion:.1f} m', True, BLACK)
    pantalla.blit(texto_posicion, (50, 150))
    
    texto_material = font.render(f'Material: {seleccion_material.capitalize()} (E = {elastic_modulus/1e9:.1f} GPa)', True, BLACK)
    pantalla.blit(texto_material, (50, 200))
    
    texto_seccion = font.render(f'Sección: {seccion.capitalize()}', True, BLACK)
    pantalla.blit(texto_seccion, (50, 250))

    pygame.display.flip()


def mostrar_diagramas(longitud, posicion, carga, modulo_elasticidad, inercia):
    """
    Argumentos:
    longitud (float): Longitud de la viga en metros
    posicion (float): Posición de la carga en metros
    carga (float): Magnitud de la carga en Newtons
    modulo_elasticidad (float): Módulo de elasticidad del material
    inercia (float): Momento de inercia de la viga
    
    Descripción:
    Muestra los diagramas de momento flector, deflexión y esfuerzo cortante usando Matplotlib
    """
    x = np.linspace(0, longitud, 500)
    
    # Reacciones en los apoyos
    R1 = carga * (longitud - posicion) / longitud
    R2 = carga - R1
    
    # Momento flector
    M = np.piecewise(x, [x <= posicion, x > posicion], 
                     [lambda x: R1 * x, lambda x: R2 * (longitud - x)])

    # Deflexión
    deflexion = np.piecewise(x, 
                              [x <= posicion, x > posicion], 
                              [lambda x: (carga * (longitud - posicion) * x**2) / (6 * modulo_elasticidad * inercia) * (3 * posicion - x),
                               lambda x: (carga * posicion * (longitud - x)**2) / (6 * modulo_elasticidad * inercia) * (3 * (longitud - posicion) - (longitud - x))])
    
    # Esfuerzo cortante
    esfuerzo_cortante = np.piecewise(x, 
                                     [x <= posicion, x > posicion], 
                                     [lambda x: R1, lambda x: -R2])

    # Graficar
    plt.figure(figsize=(10, 7))
    
    # Momento flector
    plt.subplot(3, 1, 1)
    plt.plot(x, M)
    plt.title("Diagrama de Momento Flector")
    plt.xlabel("Posición a lo largo de la viga (m)")
    plt.ylabel("Momento (Nm)")
    plt.grid(True)
    
    # Deflexión
    plt.subplot(3, 1, 2)
    plt.plot(x, deflexion, color='green')
    plt.title("Diagrama de Deflexión")
    plt.xlabel("Posición a lo largo de la viga (m)")
    plt.ylabel("Deflexión (m)")
    plt.grid(True)

    # Esfuerzo cortante
    plt.subplot(3, 1, 3)
    plt.step(x, esfuerzo_cortante, where='post', color='red')
    plt.title("Diagrama de Esfuerzos Cortantes")
    plt.xlabel("Posición a lo largo de la viga (m)")
    plt.ylabel("Esfuerzo Cortante (N)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()


def dibujar_seleccion_cajas(pantalla, materiales_rects, seccion_rects, seleccion_material, seccion, font):
    """
    Argumentos:
    pantalla (pygame.Surface): Superficie de pygame donde se dibujan las cajas
    materiales_rects (dict): Diccionario con los rectángulos de los materiales
    seccion_rects (dict): Diccionario con los rectángulos de las secciones
    seleccion_material (str): Material seleccionado actualmente
    seccion (str): Sección seleccionada actualmente
    font (pygame.font.Font): Fuente de texto para mostrar información
    
    Descripción:
    Dibuja las cajas de seleción de materiales y secciones en la pantalla
    """
    for material, rect in materiales_rects.items():
        color = GREEN if material == seleccion_material else DARK_GRAY
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, BLACK, rect, 2)
        text_surface = font.render(material.capitalize(), True, BLACK)
        pantalla.blit(text_surface, (rect.x + 10, rect.y + 10))
    
    for sec, rect in seccion_rects.items():
        color = GREEN if sec == seccion else DARK_GRAY
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, BLACK, rect, 2)
        text_surface = font.render(sec.capitalize(), True, BLACK)
        pantalla.blit(text_surface, (rect.x + 10, rect.y + 10))
