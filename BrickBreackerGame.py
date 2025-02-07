import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casse-Brique")

# Couleurs
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)

# Dimensions des objets
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_WIDTH, BRICK_HEIGHT = 75, 20

# Position initiale
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [random.choice([-4, 4]), -4]

# Création des briques
bricks = []
for row in range(5):
    for col in range(10):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Boucle du jeu
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement de la raquette
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(6, 0)

    # Déplacement de la balle
    ball.move_ip(ball_speed)

    # Collision avec les bords
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= HEIGHT:
        running = False  # Game over

    # Collision avec la raquette
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # Collision avec les briques
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            break

    # Dessin des éléments
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, RED, ball.center, BALL_RADIUS)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    # Rafraîchissement de l'écran
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
