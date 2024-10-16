import pygame
import random

pygame.init()

# Configurar la pantalla
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Viaje Espacial")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Jugador
player_width = 80
player_height = 80
player = pygame.Rect(WIDTH // 2 - player_width // 2,
                     HEIGHT - player_height - 10, player_width, player_height)

# Cargar imágenes
player_img = pygame.image.load("PYGAME/img/nave.png").convert_alpha()
meteor_img = pygame.image.load("PYGAME/img/asteroide.png").convert_alpha()
background_img = pygame.image.load("PYGAME/img/fondo.png")

player_size = (80, 80)  # Tamaño nave
meteor_size = (70, 70)  # Tamaño asteroide
background_size = (800, 600)

# Redimensionar las imágenes
player_img = pygame.transform.scale(player_img, player_size)
meteor_img = pygame.transform.scale(meteor_img, meteor_size)
background_img = pygame.transform.scale(background_img, background_size)

# Meteoritos
meteor_width = 30
meteor_height = 30
meteors = []

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

# Reloj controlar FPS
clock = pygame.time.Clock()

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Menú principal
def main_menu():
    menu_font = pygame.font.Font(None, 60)
    selected_option = 0
    options = ["Comenzar", "Controles", "Salir"]

    menu_running = True
    while menu_running:
        screen.fill(BLACK)

        # Mostrar las opciones del menú
        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (100, 100, 100)
            draw_text(option, menu_font, color, WIDTH // 2 - 100, HEIGHT // 2 - 50 + i * 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Comenzar el juego
                        menu_running = False
                    elif selected_option == 1:  # Mostrar controles
                        show_controls()
                    elif selected_option == 2:  # Salir del juego
                        pygame.quit()
                        quit()

# Mostrar controles
def show_controls():
    controls_font = pygame.font.Font(None, 40)
    controls_running = True
    while controls_running:
        screen.fill(BLACK)
        draw_text("Controles", controls_font, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 200)
        draw_text("Mover Izquierda: Flecha Izquierda", controls_font, WHITE, 100, HEIGHT // 2 - 100)
        draw_text("Mover Derecha: Flecha Derecha", controls_font, WHITE, 100, HEIGHT // 2 - 50)
        draw_text("Mover Arriba: Flecha Arriba", controls_font, WHITE, 100, HEIGHT // 2)
        draw_text("Mover Abajo: Flecha Abajo", controls_font, WHITE, 100, HEIGHT // 2 + 50)
        draw_text("Presiona 'ESC' para regresar", controls_font, WHITE, 100, HEIGHT // 2 + 150)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controls_running = False

# Bucle principal del juego
def game_loop():
    global score
    running = True
    meteors = []
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += 5

        # Generar meteoritos
        if len(meteors) < 7:
            meteor = pygame.Rect(random.randint(0, WIDTH - meteor_width),
                                 0, meteor_width, meteor_height)
            meteors.append(meteor)

        # Mover meteoritos
        for meteor in meteors:
            meteor.y += 3
            if meteor.top > HEIGHT:
                meteors.remove(meteor)
                score += 1

        # Colisiones
        for meteor in meteors:
            if player.colliderect(meteor):
                running = False

        screen.fill(BLACK)
        screen.blit(background_img, (0, 0))

        screen.blit(player_img, player)
        for meteor in meteors:
            screen.blit(meteor_img, meteor)

        # Mostrar puntuación
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Ejecutar menú principal
main_menu()
game_loop()
