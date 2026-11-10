"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    # - Comprueba que `self.level_path` existe y es fichero.
    # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    # - Guarda el resultado en `self.layout` y devuélvelo.
    if not self.level_path.is_file():
        raise FileNotFoundError("No existe el archivo del nivel")

    filas = []

    with open(self.level_path, encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n\r")
            if linea.strip():
                filas.append(linea)

    if not filas:
        raise ValueError("El nivel está vacío")

    ancho = len(filas[0])

    for fila in filas:
        if len(fila) != ancho:
            raise ValueError("Las filas tienen distinta longitud")

    self.layout = filas
    return self.layout


@arkanoid_method
def preparar_entidades(self) -> None: 
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    self.paddle = self.crear_rect(0, 0, *self.PADDLE_SIZE)

    self.paddle.midbottom = (
        self.SCREEN_WIDTH // 2, 
        self.SCREEN_HEIGHT - self.PADDLE_OFFSET 
    )
    self.score = 0 
    self.lives = 3 
    self.end_message = ""
    
    self.reiniciar_bola((1, -1))
    


@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # - Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    # - Recorre `self.layout` para detectar símbolos de bloque.
    # - Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
    self.blocks = []
    self.block_colors = []
    self.block_symbols = []

    for num_fila, fila in enumerate(self.layout):
        for num_columna, simbolo in enumerate(fila):
            if simbolo == ".":
                continue

            rectangulo = self.calcular_posicion_bloque(
                num_fila, num_columna
            )

            color = self.BLOCK_COLORS[simbolo]

            self.blocks.append(rectangulo)
            self.block_colors.append(color)
            self.block_symbols.append(simbolo)


@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    teclas = self.obtener_estado_teclas()

    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        self.paddle.x -= self.PADDLE_SPEED
        
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        self.paddle.x += self.PADDLE_SPEED
        
    if self.paddle.left < 0: 
        self.paddle.left = 0
        
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH
    
@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
    # 1. Mover la bola y obtener su rectángulo de colisión
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # 2. Rebote en paredes laterales (izquierda y derecha)
    if ball_rect.left <= 0 or ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x = -self.ball_velocity.x

    # 3. Rebote en el techo
    if ball_rect.top <= 0:
        self.ball_velocity.y = -self.ball_velocity.y

    # 4. Si la bola cae por la parte inferior de la pantalla
    if ball_rect.top >= self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives <= 0:
            self.running = False
            self.end_message = "¡Game Over!"
        else:
            self.reiniciar_bola((1, -1))
        return

    # 5. Rebote en la paleta (solo si la bola va hacia abajo)
    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        self.ball_velocity.y = -self.ball_velocity.y

    # 6. Colisión con los bloques
    for i in range(len(self.blocks)):
        if ball_rect.colliderect(self.blocks[i]):
            # Obtener el símbolo del bloque y sumar la puntuación
            simbolo = self.block_symbols[i]
            self.score += self.BLOCK_POINTS[simbolo]

            # Eliminar el bloque de las listas paralelas
            self.blocks.pop(i)
            self.block_colors.pop(i)
            self.block_symbols.pop(i)

            # Invertir la dirección vertical de la bola y salir del bucle
            self.ball_velocity.y = -self.ball_velocity.y
            break

    # 7. Comprobar si se han destruido todos los bloques
    if len(self.blocks) == 0:
        self.running = False
        self.end_message = "¡Has ganado!"

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""

    # Dibujar el fondo
    self.screen.fill(self.BACKGROUND_COLOR)

    # Dibujar los bloques
    for i in range(len(self.blocks)):
        self.dibujar_rectangulo(
            self.blocks[i],
            self.block_colors[i]
        )

    # Dibujar la paleta
    self.dibujar_rectangulo(
        self.paddle,
        self.PADDLE_COLOR
    )

    # Dibujar la bola
    self.dibujar_circulo(
        (int(self.ball_pos.x), int(self.ball_pos.y)),
        self.BALL_RADIUS,
        self.BALL_COLOR
    )

    # Dibujar puntuación y vidas
    self.dibujar_texto(
        f"Puntuación: {self.score}",
        (20, 20)
    )

    self.dibujar_texto(
        f"Vidas: {self.lives}",
        (650, 20)
    )

    self.dibujar_texto(
    "Mover: flechas / A-D | Salir: ESC",
    (20, self.SCREEN_HEIGHT - 30)
)

    # Dibujar mensaje final si existe
    if self.end_message:
        self.dibujar_texto(
            self.end_message,
            (250, 280),
            grande=True
        )



@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""

    # Inicializar pygame
    self.inicializar_pygame()

    try:
        # Preparar el juego
        self.cargar_nivel()
        self.preparar_entidades()
        self.crear_bloques()

        self.running = True

        # Bucle principal
        while self.running:

            # Comprobar eventos
            for evento in self.iterar_eventos():

                if evento.type == self.EVENT_QUIT:
                    self.running = False

                elif evento.type == self.EVENT_KEYDOWN:
                    if evento.key == self.KEY_ESCAPE:
                        self.running = False

            # Actualizar el juego si sigue activo
            if self.running:
                self.procesar_input()
                self.actualizar_bola()

            # Dibujar la escena
            self.dibujar_escena()

            # Actualizar pantalla
            self.actualizar_pantalla()

            # Controlar FPS
            self.clock.tick(self.FPS)

        #Mostrar resultado durante 3 seg
        if self.end_message:
            self.esperar(3000)

    finally:
        # Cerrar pygame
        self.finalizar_pygame()


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
