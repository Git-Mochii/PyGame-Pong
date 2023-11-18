import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window dimensions
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 650

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping-Pong Game")

# Clock for controlling frame rate
frame_rate_clock = pygame.time.Clock()

# Game variables
ball_online = False
MARGIN = 65
score_ai = 0
score_player = 0
FPS = 60
winner = 0
speed_increase_counter = 0

# Fonts and colors
FONT = pygame.font.SysFont("Arial", 35)
BACKGROUND_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)

# Function to set the window style
def set_window_style():
    window.fill(BACKGROUND_COLOR)
    pygame.draw.line(window, WHITE, (0, MARGIN), (WINDOW_WIDTH, MARGIN))

# Function to display text on the window
def display_text(text, font, color, x, y):
    image = font.render(text, True, color)
    window.blit(image, (x, y))

# Class for the player's paddle
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 20, 100)
        self.speed = 8

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > MARGIN:
            self.rect.move_ip(0, -1 * self.speed)
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0, self.speed)

    def ai_move(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0, self.speed)
        if self.rect.centery > pong.rect.bottom and self.rect.top > MARGIN:
            self.rect.move_ip(0, -1 * self.speed)

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

# Class for the ball
class Ball:
    def __init__(self, x, y):
        self.restart(x, y)

    def move(self):
        if self.rect.top < MARGIN or self.rect.bottom > WINDOW_HEIGHT:
            self.speed_y *= -1

        if self.rect.colliderect(paddle_player.rect):
            self.speed_x *= -1
        if self.rect.colliderect(paddle_ai.rect):
            self.speed_x *= -1

        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > WINDOW_WIDTH:
            self.winner = -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(window, WHITE, (self.rect.x + self.radius * 2, self.rect.y + self.radius), self.radius)

    def restart(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.speed_x = -3
        self.speed_y = 3
        self.winner = 0

# Initialize Game Objects
pong = Ball(WINDOW_WIDTH - 80, WINDOW_HEIGHT // 2 + 50)
paddle_player = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2)
paddle_ai = Paddle(20, WINDOW_HEIGHT // 2)

# Main game loop
run = True
game_started = False  # Variable to track whether the game has started or not

while run:
    frame_rate_clock.tick(FPS)  # FPS

    set_window_style()  # Style

    paddle_player.move()  # Player movement action enabled
    winner = pong.move()  # Ball movement position determines winner

    paddle_player.draw()  # Display Player Paddle
    paddle_ai.draw()  # Display AI Paddle

    # Ball Logic for when the game runs/ends (1 = player scores, -1 = AI scores, 0 = Game hasn't begun)
    if game_started:
        speed_increase_counter += 1
        winner = pong.move()
        if winner == 0:
            paddle_player.move()
            paddle_ai.ai_move()
            pong.draw()
        else:
            game_started = False
            if winner == 1:
                score_player += 1
            elif winner == -1:
                score_ai += 1

    # Guide for Player
    if not game_started:
        display_text("CLICK TO PLAY", FONT, WHITE, 245, WINDOW_HEIGHT // 2 - 100)

    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            game_started = True
            ball_online = True  # Start ball movement
            pong.restart(WINDOW_WIDTH - 80, WINDOW_HEIGHT // 2 + 50)

    # Logic for Ball speed increase
    if speed_increase_counter > 500:
        speed_increase_counter = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1
        if pong.speed_x > 0:
            pong.speed_x += 1

        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1

    # Display scores and game information
    display_text("AI: " + str(score_ai), FONT, WHITE, 20, 15)
    display_text("Player: " + str(score_player), FONT, WHITE, WINDOW_WIDTH - 160, 15)
    display_text("Ping-Pong Speed: " + str(abs(pong.speed_x)), FONT, WHITE, WINDOW_WIDTH // 2 - 160, 15)

    pygame.display.update()

# Quit Pygame when the game loop ends
pygame.quit()