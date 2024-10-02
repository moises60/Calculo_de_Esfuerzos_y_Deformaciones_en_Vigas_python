import pygame
import random

def cargar_imagen(ruta, ancho=None, alto=None):
    """
    Argumentos:
        ruta (str): La ruta del archivo de imagen a cargar.
        ancho (int, opcional): El nuevo ancho de la imagen. Si es None, se mantiene el original.
        alto (int, opcional): El nuevo alto de la imagen. Si es None, se mantiene el original.
    
    Descripción:
        Carga una imagen desde la ruta especificada y la redimensiona si se especifican las dimensionees.
    """
    imagen = pygame.image.load(ruta).convert_alpha()
    if ancho and alto:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return imagen


def dibujar_texto(superficie, texto, tamaño, x, y):
    """
    Argumntos:
        superficie (pygame.Surface): La superficie en la que se dibuja el texto.
        texto (str): El texto que se va a mostrar.

        tamaño (int): El tamaño de la fuente del texto.
        x (int): La posición X en la superficie.
        y (int): La posición Y en la superficie.

    Descripción:
        Dibuja un texto en la pantalla en la posición especificada.
    """
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, (0, 0, 0))
    superficie.blit(superficie_texto, (x, y))


def generar_obstaculo(ancho_pantalla, alto_pantalla, nivel_dificultad):
    """
    Argumentos:
        ancho_pantalla (int): El ancho de la pantalla del juego.
        alto_pantalla (int): El alto de la pantalla del juego.
        nivel_dificultad (int): Nivel de dificultad que afecta la distancia mínima entre obstáculos.
    
    Descripción:
        Genera un nuevo obstáculo en una posición aleatoria dentro de la pantalla del juego.
        La forma del obstáculo es aleatoria (triángulo, rectángulo, cuadrado o círculo).
    """
    # Definir lus obstáculos
    formas = ["rectangulo", "cuadrado", "circulo", "triangulo"]
    forma = random.choice(formas)
    
    
    altura_base = alto_pantalla - 100  
    
    if forma == "rectangulo":
        ancho = random.randint(20, 40)

        alto = random.randint(50, 58)
        obstaculo = pygame.Rect(ancho_pantalla, altura_base - alto, ancho, alto)
    elif forma == "cuadrado":
        tamano = random.randint(30, 50)
        obstaculo = pygame.Rect(ancho_pantalla, altura_base - tamano, tamano, tamano)
    elif forma == "circulo":
        radio = random.randint(15, 30)
        obstaculo = (forma, ancho_pantalla, altura_base -2*radio, radio)
    elif forma == "triangulo":
        base = random.randint(30, 50)

        altura = random.randint(40, 60)
        obstaculo = (forma, ancho_pantalla, altura_base - altura, base, altura)

    return obstaculo


def dibujar_obstaculo(pantalla, obstaculo):
    """
    Argumentos:
        pantalla (pygame.Surface): La superficie en la que se dibuja el obstáculo.
        obstaculo (tuple or pygame.Rect): El obstáculo que se va a dibujar. 
                                    Puede ser un Rect o una tupla para formas personalizadas.
    
    Descripción:
        Dibuja un obstáculo en la pantalla dependiendo de su forma.
    """
    if isinstance(obstaculo, pygame.Rect):
        pygame.draw.rect(pantalla, (0, 0, 0), obstaculo)
    else:
        forma = obstaculo[0]
        if forma == "circulo":
            _, x, y, radio = obstaculo
            pygame.draw.circle(pantalla, (0, 0, 0), (x + radio, y + radio), radio)
        elif forma == "triangulo":
            _, x, y, base, altura = obstaculo
            puntos = [(x, y + altura), (x + base // 2, y), (x + base, y + altura)]
            pygame.draw.polygon(pantalla, (0, 0, 0), puntos)


def mover_obstaculos(obstaculos, velocidad):
    """
    Argumentos:
        obstaculos (list): Una lista de obstáculos representados por objetos Rect o tuplas para otras formas.
        velocidad (int): La velocidad a la que los obstáculos se mueven hacia la izquierda.
    
    Descripción:
        Mueve todos los obstáculos hacia la izquierda a la velocidad especificada.
    """
    for i, obstaculo in enumerate(obstaculos):
        if isinstance(obstaculo, pygame.Rect):
            obstaculo.x -= velocidad
        else:
            forma, x, y, *dimensiones = obstaculo
            x -= velocidad
            if forma == "circulo":
                obstaculos[i] = (forma, x, y, dimensiones[0])
            elif forma == "triangulo":
                obstaculos[i] = (forma, x, y, dimensiones[0], dimensiones[1])



def detectar_colision(conejo, obstaculos):
    """
    Argumentos:
        conejo (pygame.Rect): Un objeto Rect que representa al conejo.
        obstaculos (list): Una lista de obstáculos representados por objetos Rect o tuplas.
    
    Descripción:
        Detecta si el conejo ha colisionado con algún obstáculo.
    """
    for obstaculo in obstaculos:
        if isinstance(obstaculo, pygame.Rect):
            if conejo.colliderect(obstaculo):
                return True
        else:
            forma = obstaculo[0]
            if forma == "circulo":
                _, x, y, radio = obstaculo
                # Detectar colisión con el círculo usando distanciia
                distancia_x = conejo.centerx - (x + radio)
                distancia_y = conejo.centery - (y + radio)
                distancia = (distancia_x**2 + distancia_y**2) ** 0.5
                if distancia < radio + conejo.width / 2:  # Colisión si la distancia es menor que el radio más la mitad del ancho del conjo
                    return True
            elif forma == "triangulo":
                _, x, y, base, altura = obstaculo
                # Para la colisión con triángulos, se usa un bounding box rectangular simple
                # que rodea el triángulo como aproximación.
                rectangulo_triangulo = pygame.Rect(x, y, base, altura)
                if conejo.colliderect(rectangulo_triangulo):
                    return True
    return False
