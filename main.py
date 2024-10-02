import pygame
import sys
from funciones import cargar_imagen, dibujar_texto, generar_obstaculo, mover_obstaculos, detectar_colision, dibujar_obstaculo
import random

pygame.init()

ancho_pantalla = 1000
alto_pantalla = 500
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego de Saltar Obstáculos")

# Configuración del reloj
reloj = pygame.time.Clock()


# Cargar imágenes
imagen_conejo_1 = cargar_imagen("assets/conejo.png", ancho=50, alto=50)
imagen_conejo_2 = cargar_imagen("assets/conejo2.png", ancho=50, alto=50)
imagen_fondo = cargar_imagen("assets/fondo.png", ancho=ancho_pantalla, alto=alto_pantalla)
# Inicializar una variable para controlar el estado de la animacion del coneji
contador_animacion = 0

# Inicializar variables del juego
conejo = pygame.Rect(100, alto_pantalla - 150, 50, 50)  # Altura inicial del conejo
gravedad = 1.1
velocidad_salto = -18
velocidad_conejo = 0
obstaculos = []
velocidad_juego = 5
puntuacion = 0
juego_iniciado = False  # Controla si el juego ha comenzado para empezar a contar


nivel_dificultad = "Fácil"  # Nivel de dificultad inicial
distancia_minima = 300  # Distancia mínima inicial entre obstáculos
distancia_maxima = 500  # Distancia máxima inicial entre obstáculos

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if not juego_iniciado:
                    juego_iniciado = True  
                if conejo.y == alto_pantalla - 150:  # Solo permitir saltar si está en el suelo
                    velocidad_conejo = velocidad_salto

    # Actualizar posición del conejo solo si el juego ha comenzado
    if juego_iniciado:
        velocidad_conejo += gravedad
        conejo.y += velocidad_conejo

    if conejo.y > alto_pantalla - 150:
        conejo.y = alto_pantalla - 150
        velocidad_conejo = 0

    # Actualizar el contador de animación
    contador_animacion += 1
    if contador_animacion >= 10:  # velocidad de la animación
        contador_animacion = 0

    # Seleccionar la imagen del conejo en función del contador de animaciun
    if contador_animacion < 5:
        imagen_conejo_actual = imagen_conejo_1
    else:
        imagen_conejo_actual = imagen_conejo_2

    # Generar nuevos obstáculos y moverlos solo si el juego ha comenzado
    if juego_iniciado:
        ultimo_obstaculo = obstaculos[-1] if obstaculos else None
        if len(obstaculos) == 0 or (
            isinstance(ultimo_obstaculo, pygame.Rect) and ultimo_obstaculo.x < ancho_pantalla - random.randint(distancia_minima, distancia_maxima)
        ) or (
            isinstance(ultimo_obstaculo, tuple) and ultimo_obstaculo[1] < ancho_pantalla - random.randint(distancia_minima, distancia_maxima)
        ):
            obstaculos.append(generar_obstaculo(ancho_pantalla, alto_pantalla, nivel_dificultad))

        mover_obstaculos(obstaculos, velocidad_juego)

        # Detectar colisión
        if detectar_colision(conejo, obstaculos):
            print(f"¡Colisión! Puntuación final: {puntuacion}")
            dibujar_texto(pantalla, f"Puntuación Final: {puntuacion}", 48, ancho_pantalla // 2 - 100, alto_pantalla // 2)
            pygame.display.flip()
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()

    # Dibujar todo en la pantala
    pantalla.blit(imagen_fondo, (0, 0))
    pantalla.blit(imagen_conejo_actual, (conejo.x, conejo.y)) 
    for obstaculo in obstaculos:

        dibujar_obstaculo(pantalla, obstaculo)
    
    # Actualizar la puntuación solo si el juego ha comenzado
    if juego_iniciado:
        puntuacion += 1
    dibujar_texto(pantalla, f"Puntuación: {puntuacion}", 36, 10, 10)
    dibujar_texto(pantalla, f"Nivel: {nivel_dificultad}", 36, ancho_pantalla - 150, 10)

    # Actualizar la pantalla
    pygame.display.flip()
    
    # Limitar a 30 FPS
    reloj.tick(30)