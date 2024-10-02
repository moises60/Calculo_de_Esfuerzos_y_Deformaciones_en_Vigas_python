import pygame
from funciones import (
    calcular_inercia,
    dibujar_viga,
    mostrar_diagramas,
    dibujar_seleccion_cajas,
    materiales,
    validar_entrada_numerica,
    guardar_configuracion,
    cargar_configuracion,
)

import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Vigas Interactivo")

# Inicializar la fuentee
font = pygame.font.Font(None, 30)

# Variables iniciales
longitud = 10.0  # Longitud en metros
posicion_carga = 5.0  # Posición de la carga
carga = 1000.0  # Magnitud de la carga en Newtons
texto_carga = str(carga)  # Mantener el texto de la carga ingresada
input_activo = False
input_field = None  # Campo de entrada activo
seccion = 'rectangular'
seleccion_material = 'acero'
elastic_modulus = materiales[seleccion_material]
inercia = calcular_inercia(seccion)
guardar_cargar_flag = False

# Rectángulos para la selección
materiales_rects = {
    'acero': pygame.Rect(50, 350, 150, 40),
    'madera': pygame.Rect(220, 350, 150, 40),
    'aluminio': pygame.Rect(390, 350, 150, 40),
}
seccion_rects = {
    'rectangular': pygame.Rect(50, 400, 150, 40),
    'circular': pygame.Rect(220, 400, 150, 40),
    'I': pygame.Rect(390, 400, 150, 40),
}

# Botones
boton_guardar = pygame.Rect(50, 450, 150, 40)
boton_cargar = pygame.Rect(220, 450, 150, 40)

# Variables de control
arrastrando_carga = False
arrastrando_longitud = False
mostrar_diagramas_flag = False

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hace clic en el campo de carga
            if 50 <= event.pos[0] <= 200 and 100 <= event.pos[1] <= 130:
                input_activo = True
                input_field = 'carga'
            # Verificar si se hace clic en el campo de longitud
            elif 50 <= event.pos[0] <= 200 and 140 <= event.pos[1] <= 170:
                input_activo = True
                input_field = 'longitud'
            else:
                input_activo = False
                input_field = None

            # Verificar si se hace clic en la carga para arrastrarla
            if (
                100 + posicion_carga * 50 - 10 <= event.pos[0] <= 100 + posicion_carga * 50 + 10
                and HEIGHT // 2 - 60 <= event.pos[1] <= HEIGHT // 2
            ):
                arrastrando_carga = True

            # Verificar si se hace clic en el extremo derecho de la viga para modificar la longitud
            if (
                100 + longitud * 50 - 10 <= event.pos[0] <= 100 + longitud * 50 + 10
                and HEIGHT // 2 - 20 <= event.pos[1] <= HEIGHT // 2 + 20
            ):
                arrastrando_longitud = True

            # Verificar si se selecciona un material
            for material, rect in materiales_rects.items():
                if rect.collidepoint(event.pos):
                    seleccion_material = material
                    elastic_modulus = materiales[seleccion_material]

            # Verificar si se selecciona una sección
            for sec, rect in seccion_rects.items():
                if rect.collidepoint(event.pos):
                    seccion = sec
                    inercia = calcular_inercia(seccion)

            # Botones de guardar y cargar
            if boton_guardar.collidepoint(event.pos):
                guardar_configuracion(
                    longitud,
                    posicion_carga,
                    carga,
                    seleccion_material,
                    seccion,
                )
            if boton_cargar.collidepoint(event.pos):
                (
                    longitud,
                    posicion_carga,
                    carga,
                    seleccion_material,
                    seccion,
                ) = cargar_configuracion()
                elastic_modulus = materiales[seleccion_material]
                inercia = calcular_inercia(seccion)

        if event.type == pygame.MOUSEBUTTONUP:
            arrastrando_carga = False
            arrastrando_longitud = False

        if event.type == pygame.MOUSEMOTION:
            if arrastrando_carga:
                nueva_posicion = (event.pos[0] - 100) / 50
                nueva_posicion = max(0, min(longitud, nueva_posicion))
                posicion_carga = nueva_posicion

            if arrastrando_longitud:
                longitud = (event.pos[0] - 100) / 50
                longitud = max(5, min(20, longitud))
                # Ajustar posición de la carga si excede la nueva longitud
                posicion_carga = min(posicion_carga, longitud)

        if event.type == pygame.KEYDOWN:
            if input_activo:
                if event.key == pygame.K_BACKSPACE:
                    if input_field == 'carga':
                        texto_carga = texto_carga[:-1]
                    elif input_field == 'longitud':
                        texto_longitud = texto_longitud[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    if input_field == 'carga':
                        texto_carga += event.unicode
                    elif input_field == 'longitud':
                        texto_longitud += event.unicode
                if event.key == pygame.K_RETURN:
                    if input_field == 'carga' and validar_entrada_numerica(texto_carga):
                        carga = float(texto_carga)
                    elif input_field == 'longitud' and validar_entrada_numerica(texto_longitud):
                        longitud = float(texto_longitud)
                        longitud = max(5, min(20, longitud))
                        # Ajustar posición de la carga si excede la nueva longitud
                        posicion_carga = min(posicion_carga, longitud)
                    input_activo = False
                    input_field = None

            if event.key == pygame.K_RETURN and not input_activo:
                mostrar_diagramas_flag = True

    # Dibujar todos los elementos.
    dibujar_viga(
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
    )

    # Mostrar los diagramas al presionar Enter
    if mostrar_diagramas_flag:
        mostrar_diagramas(
            longitud, posicion_carga, carga, elastic_modulus, inercia
        )
        mostrar_diagramas_flag = False

pygame.quit()
sys.exit()
