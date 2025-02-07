import pygame
import random

# Initialisation de pygame
pygame.init()

# Paramètres de l'écran
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Vitesse du jeu
clock = pygame.time.Clock()
FPS = 60

# Charger les sons
bounce_sound = pygame.mixer.Sound("sounds/bounce.mp3")
brick_break_sound = pygame.mixer.Sound("sounds/brick_break.mp3")
game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")

# Class pour la balle
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 10
        self.color = WHITE
        self.x_velocity = 4 * random.choice((1, -1))
        self.y_velocity = -4

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.x_velocity = -self.x_velocity
            bounce_sound.play()

        if self.y <= self.radius:
            self.y_velocity = -self.y_velocity
            bounce_sound.play()

        if self.y >= HEIGHT - self.radius:
            return True  # Si la balle touche le bas, retourner True (Game Over)
        return False

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_velocity = 4 * random.choice((1, -1))
        self.y_velocity = -4

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Classe pour la raquette
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - self.height - 10
        self.color = WHITE
        self.velocity = 8

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.velocity
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Classe pour les briques
class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.x = x
        self.y = y
        self.color = GREEN
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Fonction pour afficher le score
def show_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Fonction pour afficher "Game Over"
def game_over():
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
    pygame.display.update()
    game_over_sound.play()

# Fonction principale du jeu
def main():
    score = 0
    game_running = True

    ball = Ball()
    paddle = Paddle()

    # Création des briques
    bricks = []
    for row in range(5):
        for col in range(10):
            brick = Brick(col * 60 + 10, row * 20 + 50)
            bricks.append(brick)

    while game_running:
        screen.fill(BLACK)

        # Afficher les briques
        for brick in bricks:
            brick.draw(screen)

        # Détecter les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Contrôles de la raquette
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Déplacer la balle
        if ball.move():
            game_over()
            pygame.time.wait(2000)
            ball.reset()
            score = 0
            bricks.clear()
            for row in range(5):
                for col in range(10):
                    brick = Brick(col * 60 + 10, row * 20 + 50)
                    bricks.append(brick)

        # Collision balle/raquette
        if ball.y + ball.radius >= paddle.y and paddle.x <= ball.x <= paddle.x + paddle.width:
            ball.y_velocity = -ball.y_velocity
            bounce_sound.play()

        # Collision balle/brique
        for brick in bricks[:]:
            if brick.rect.colliderect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2):
                bricks.remove(brick)
                score += 10
                brick_break_sound.play()

        # Affichage du score et de la balle
        show_score(score)
        ball.draw(screen)
        paddle.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
