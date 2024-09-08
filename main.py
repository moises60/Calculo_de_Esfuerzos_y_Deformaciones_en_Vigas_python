import pygame
from funciones import calcular_inercia, dibujar_viga, mostrar_diagramas, dibujar_seleccion_cajas, materiales

# Inicialización de pygame
pygame.init()
pygame.font.init()  

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Vigas")

# Inicializar la fuente
font = pygame.font.Font(None, 36)

# Variables iniciales
longitud = 10
posicion = 5
carga = 1000
texto_carga = str(carga)  # Mantener el texto de la carga ingresada
input_activo = False  
seccion = 'rectangular'
seleccion_material = 'acero'
elastic_modulus = materiales[seleccion_material]
inercia = calcular_inercia(seccion)

# Rectángulos para la selección
materiales_rects = {'acero': pygame.Rect(50, 300, 150, 50),
                    'madera': pygame.Rect(250, 300, 150, 50),
                    'aluminio': pygame.Rect(450, 300, 150, 50)}
seccion_rects = {'rectangular': pygame.Rect(50, 400, 150, 50),
                 'circular': pygame.Rect(250, 400, 150, 50)}

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
            # Verificar si se hace clic en el texto de la carga para activarlo
            if 50 <= event.pos[0] <= 190 and 100 <= event.pos[1] <= 140:
                input_activo = True  # Activar el cuadro de texto
            else:
                input_activo = False

            # Verificar si se hace clic en la carga para arrastrarla
            if 100 + posicion * 50 - 10 <= event.pos[0] <= 100 + posicion * 50 + 10 and HEIGHT//2 - 60 <= event.pos[1] <= HEIGHT//2:
                arrastrando_carga = True
            
            # Verificar si se hace clic en el extremo derecho de la viga para modificar la longitud
            if 100 + longitud * 50 - 10 <= event.pos[0] <= 100 + longitud * 50 + 10 and HEIGHT//2 - 20 <= event.pos[1] <= HEIGHT//2 + 20:
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

        if event.type == pygame.MOUSEBUTTONUP:
            arrastrando_carga = False
            arrastrando_longitud = False

        if event.type == pygame.MOUSEMOTION:
            if arrastrando_carga:
                posicion = (event.pos[0] - 100) / 50
                posicion = max(0, min(longitud, posicion))

            if arrastrando_longitud:
                longitud = (event.pos[0] - 100) / 50
                longitud = max(5, min(20, longitud))

        if event.type == pygame.KEYDOWN:
            if input_activo:
                # Permitir solo números y borrar el texto con la tecla de retroceso
                if event.key == pygame.K_BACKSPACE:
                    texto_carga = texto_carga[:-1]
                elif event.unicode.isdigit():
                    texto_carga += event.unicode
                # Actualizar la carga cuando se presione Enter
                if event.key == pygame.K_RETURN and texto_carga:
                    carga = int(texto_carga)
                    input_activo = False  # Desactivar cuadro de texto después de presionar Enter

            if event.key == pygame.K_RETURN and not input_activo:
                mostrar_diagramas_flag = True


    # Dibujar todos los elementos. 
    dibujar_viga(pantalla, longitud, posicion, carga, seleccion_material, seccion, elastic_modulus, font,materiales_rects,seccion_rects)


    # Mostrar los diagramas al presionar Enter
    if mostrar_diagramas_flag:
        mostrar_diagramas(longitud, posicion, carga, elastic_modulus, inercia)
        mostrar_diagramas_flag = False

pygame.quit()
