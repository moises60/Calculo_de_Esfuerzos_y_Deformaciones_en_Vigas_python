import pygame
import matplotlib.pyplot as plt
import numpy as np
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

# Materiales comunes
# Módulo de elasticidad en Pascales
materiales = {
    'acero': 210e9,      
    'madera': 11e9,
    'aluminio': 69e9,
}

def calcular_inercia(seccion):
    """
    Argumentos:
    seccion (str): Sección de la viga (rectangular, circular, I)

    Descripción:
    Calcula el momento de inercia de la viga según la sección transversal.
    Devuelve el momento de inercia en metros a la cuarta potencia (m^4).
    """
    if seccion == 'rectangular':
        base = 0.2  # metros
        altura = 0.3  # metros
        return (base * altura**3) / 12
    elif seccion == 'circular':
        radio = 0.15  # metros
        return (np.pi * radio**4) / 4
    elif seccion == 'I':
        altura = 0.3  # metros
        ancho_alma = 0.02  # metros
        ancho_ala = 0.1  # metros
        espesor_ala = 0.02  # metros
        I = (ancho_ala * altura**3 / 12) - ((ancho_ala - ancho_alma) * (altura - 2 * espesor_ala)**3 / 12)
        return I

def validar_entrada_numerica(texto):
    """
    Verifica si el texto ingresado es un número válido.

    Argumentos:
    texto (str): Texto ingresado por el usuario.

    """
    try:
        float(texto)
        return True
    except ValueError:
        return False

def dibujar_viga(
    pantalla,
    longitud,
    posicion_carga,
    carga,
    seleccion_material,
    seccion,
    elastic_modulus,
    font,
    materiales_rects,
    seccion_rects,
    boton_guardar,
    boton_cargar,
):
    """
    Argumentos:
    pantalla (pygame.Surface): La superficie de pygame donde se dibuja la viga.
    longitud (float): Longitud de la viga en metros.
    posicion_carga (float): Posición de la carga en metros.
    carga (float): Magnitud de la carga en Newtons.
    seleccion_material (str): Material seleccionado (acero, madera, aluminio).
    seccion (str): Sección transversal de la viga.
    elastic_modulus (float): Módulo de elasticidad del material en Pascales.
    font (pygame.font.Font): Fuente de texto para mostrar información.
    materiales_rects (dict): Diccionario con los rectángulos de los materiales.
    seccion_rects (dict): Diccionario con los rectángulos de las secciones.
    boton_guardar (pygame.Rect): Rectángulo del botón de guardar.
    boton_cargar (pygame.Rect): Rectángulo del botón de cargar.

    Descripción:
    Dibuja la viga, la carga aplicada, botones de guardar/cargar y muestra información relevante en la pantalla.
    """
    pantalla.fill(WHITE)
    dibujar_seleccion_cajas(
        pantalla, materiales_rects, seccion_rects, seleccion_material, seccion, font
    )

    # Botones de guardar y cargar
    pygame.draw.rect(pantalla, LIGHT_GRAY, boton_guardar)
    pygame.draw.rect(pantalla, BLACK, boton_guardar, 2)
    texto_guardar = font.render("Guardar", True, BLACK)
    pantalla.blit(
        texto_guardar,
        (boton_guardar.x + 20, boton_guardar.y + 10),
    )

    pygame.draw.rect(pantalla, LIGHT_GRAY, boton_cargar)
    pygame.draw.rect(pantalla, BLACK, boton_cargar, 2)
    texto_cargar = font.render("Cargar", True, BLACK)
    pantalla.blit(
        texto_cargar,
        (boton_cargar.x + 30, boton_cargar.y + 10),
    )

    # Dibuja la viga
    pygame.draw.rect(
        pantalla, GRAY, (100, pantalla.get_height() // 2 - 20, longitud * 50, 20)
    )

    # Dibujar la carga
    pygame.draw.line(
        pantalla,
        BLUE,
        (100 + posicion_carga * 50, pantalla.get_height() // 2 - 50),
        (100 + posicion_carga * 50, pantalla.get_height() // 2),
        5,
    )
    pygame.draw.polygon(
        pantalla,
        BLUE,
        [
            (100 + posicion_carga * 50, pantalla.get_height() // 2 - 60),
            (95 + posicion_carga * 50, pantalla.get_height() // 2 - 50),
            (105 + posicion_carga * 50, pantalla.get_height() // 2 - 50),
        ],
    )

    # Mostrar textos de información
    texto_longitud = font.render(f'Longitud: {longitud:.1f} m', True, BLACK)
    pantalla.blit(texto_longitud, (50, 50))

    texto_carga_display = font.render(
        f'Carga: {carga:.1f} N', True, BLACK
    )
    pantalla.blit(texto_carga_display, (50, 100))

    texto_posicion = font.render(
        f'Posición de la carga: {posicion_carga:.1f} m', True, BLACK
    )
    pantalla.blit(texto_posicion, (50, 150))

    texto_material = font.render(
        f'Material: {seleccion_material.capitalize()} (E = {elastic_modulus/1e9:.1f} GPa)',
        True,
        BLACK,
    )
    pantalla.blit(texto_material, (50, 200))

    texto_seccion = font.render(f'Sección: {seccion.capitalize()}', True, BLACK)
    pantalla.blit(texto_seccion, (50, 250))

    pygame.display.flip()

def mostrar_diagramas(
    longitud, posicion_carga, carga, modulo_elasticidad, inercia
):
    """
    Argumentos:
    longitud (float): Longitud de la viga en metros.
    posicion_carga (float): Posición de la carga en metros.
    carga (float): Magnitud de la carga en Newtons.
    modulo_elasticidad (float): Módulo de elasticidad del material en Pascales.
    inercia (float): Momento de inercia de la viga en metros a la cuarta potencia (m^4).

    Descripción:
    Muestra los diagramas de momento flector, deflexión y esfuerzo cortante usando Matplotlib.
    """
    x = np.linspace(0, longitud, 500)

    # Reacciones en los apoyos (soportes simples)
    R1 = carga * (longitud - posicion_carga) / longitud
    R2 = carga - R1

    # Momento flector
    M = np.piecewise(x, [x <= posicion_carga, x > posicion_carga],
                    [lambda x: R1 * x, lambda x: R1 * x - carga * (x - posicion_carga)])

    # Esfuerzo cortante
    V = np.piecewise(x, [x <= posicion_carga, x > posicion_carga],
                    [lambda x: R1, lambda x: R1 - carga])

    # Deflexión (Integración numérica)
    EI = modulo_elasticidad * inercia
    theta = np.zeros_like(x)
    deflexion = np.zeros_like(x)
    for i in range(1, len(x)):
        dx = x[i] - x[i - 1]
        theta[i] = theta[i - 1] + (M[i - 1] / EI) * dx
        deflexion[i] = deflexion[i - 1] + theta[i - 1] * dx

    # Graficar
    plt.figure(figsize=(10, 8))

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
    plt.step(x, V, where='post', color='red')
    plt.title("Diagrama de Esfuerzos Cortantes")
    plt.xlabel("Posición a lo largo de la viga (m)")
    plt.ylabel("Esfuerzo Cortante (N)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def dibujar_seleccion_cajas(
    pantalla, materiales_rects, seccion_rects, seleccion_material, seccion, font
):
    """
    Argumentos:
    pantalla (pygame.Surface): Superficie de pygame donde se dibujan las cajas.
    materiales_rects (dict): Diccionario con los rectángulos de los materiales.
    seccion_rects (dict): Diccionario con los rectángulos de las secciones.
    seleccion_material (str): Material seleccionado actualmente.
    seccion (str): Sección seleccionada actualmente.
    font (pygame.font.Font): Fuente de texto para mostrar información.

    Descripción:
    Dibuja las cajas de selección de materiales y secciones en la pantalla.
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

def guardar_configuracion(
    longitud, posicion_carga, carga, seleccion_material, seccion
):
    """
    Guarda la configuración actual en un archivo JSON.

    Argumentos:
    longitud (float): Longitud de la viga en metros.
    posicion_carga (float): Posición de la carga en metros.
    carga (float): Magnitud de la carga en Newtons.
    seleccion_material (str): Material seleccionado.
    seccion (str): Sección transversal seleccionada.

    Descripción:
    Guarda la configuración actual de la viga en un archivo JSON para uso futuro.
    """
    configuracion = {
        'longitud': longitud,
        'posicion_carga': posicion_carga,
        'carga': carga,
        'material': seleccion_material,
        'seccion': seccion,
    }
    with open('configuracion_viga.json', 'w') as file:
        json.dump(configuracion, file)
    print("Configuración guardada exitosamente.")

def cargar_configuracion():
    """
    Carga la configuración desde un archivo JSON.

    Retorna:
    tuple: (longitud, posicion_carga, carga, seleccion_material, seccion)
    """
    try:
        with open('configuracion_viga.json', 'r') as file:
            configuracion = json.load(file)
        print("Configuración cargada exitosamente.")
        return (
            configuracion['longitud'],
            configuracion['posicion_carga'],
            configuracion['carga'],
            configuracion['material'],
            configuracion['seccion'],
        )
    except FileNotFoundError:
        print("No se encontró ninguna configuración guardada.")
        return (10.0, 5.0, 1000.0, 'acero', 'rectangular')
