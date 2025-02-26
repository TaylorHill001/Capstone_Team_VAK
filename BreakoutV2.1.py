import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
ROWS = 5
COLS = 9
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#Scores
scores = [
    ("Alice", 5000, 10),
    ("Bob", 4200, 9),
    ("Charlie", 3900, 8),
    ("David", 3500, 7),
    ("Eve", 3000, 6),
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Arcade Game")
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40), (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.speed = 10

    def move(self, direction):
        if direction == "LEFT" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "RIGHT" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self, speed):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.dx = random.choice([-speed, speed])
        self.dy = -speed
        self.speed = speed

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)


# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = random.choice([RED, GREEN, BLUE])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

# Create bricks
def create_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (BRICK_WIDTH + 10) + 35
            y = row * (BRICK_HEIGHT + 10) + 50
            bricks.append(Brick(x, y))
    return bricks

# Display retry popup
def show_retry_popup():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over! Try Again?", True, RED)
    retry_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    yes_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 100, 50)
    no_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 90, 50)

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(text, retry_rect)

        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)

        yes_text = font.render("Yes", True, WHITE)
        no_text = font.render("No", True, WHITE)

        yes_text_rect = yes_text.get_rect(center=yes_button.center)
        no_text_rect = no_text.get_rect(center=no_button.center)

        screen.blit(yes_text, yes_text_rect)
        screen.blit(no_text, no_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(event.pos):
                    return True
                if no_button.collidepoint(event.pos):
                    return False
                




#Menu fuctionality 

#Main Menu
#Looks for any key press to start game. 
def show_main_menu():
    font = pygame.font.Font(None, 50)
    text = font.render("Breakout Game", True, BLUE)
    subtext = font.render("Press any key to continue", True, GREEN)

    while True:
       
        screen.fill(BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                return  

#Pause Menu
#Looks for "P" key press to pause. Use any key to resume the game. 
def pause_menu():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Paused", True, RED)
    subtext = font.render("Press any key to resume", True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return  


#Start timer
#Creates the delay so players can get ready.
def menu_timer():
    font = pygame.font.SysFont('Consolas', 50)
    counter = 3  # Countdown from 3
    clock = pygame.time.Clock()

    while counter > 0:
        screen.fill(WHITE)  # Clear screen
        text = font.render(str(counter), True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)  # Draw countdown
        
        pygame.display.flip()  # Update screen
        pygame.time.delay(1000)  # Wait 1 second
        counter -= 1  # Decrease counter

    screen.fill(WHITE)  # Clear the countdown after finishing
    pygame.display.flip()



#Scoring Menu
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Scores")

# Load font
font = pygame.font.Font(None, 50)

# Hardcoded scores (no file parsing at this time)

def draw_scores():
    """Renders and displays the scores on the screen."""
    screen.fill(BLACK)  

    title_text = font.render("Top Scores", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    subtext = font.render("Press any key to continue", True, GREEN)
    screen.blit(title_text, title_rect)
    screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 1.4))

    while True:

        # Draw scores
        for i, (name, score, level) in enumerate(scores):
            score_text = font.render(f"{i+1}. {name}: {score} (Lvl {level})", True, BLUE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180 + i * 50))
            screen.blit(score_text, score_rect)

        pygame.display.flip()  

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    return 






# Main game loop
def main():
    #Main menu only appears at start of the game. 
    # Will not show again after level pass or restart. 
    show_main_menu() 

    level = 1
    ball_speed = 4

    while True:  # Game loop for restarting levels


        draw_scores() #Scores show up before each game begins
        menu_timer() #Count down timer gives players time to prepare to play. 
        paddle = Paddle()
        ball = Ball(ball_speed)
        bricks = create_bricks()

        running = True  # Ensure game loop resets for each level

        while running:
            
            screen.fill(WHITE)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("LEFT")
            if keys[pygame.K_RIGHT]:
                paddle.move("RIGHT")

            # Ball movement
            ball.move()

            # Ball collision with paddle (adjust angle based on impact position)
            if ball.rect.colliderect(paddle.rect):
                offset = (ball.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
                ball.dy = -ball.speed
                ball.dx = ball.speed * offset  # Adjust angle based on impact position

            # Ball collision with bricks
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    bricks.remove(brick)

                    # Determine collision direction
                    if abs(ball.rect.bottom - brick.rect.top) < 10 or abs(ball.rect.top - brick.rect.bottom) < 10:
                        ball.dy *= -1  # Vertical collision
                    else:
                        ball.dx *= -1  # Horizontal collision
                    break  # Only break out of brick collision loop, not the game loop

            # **Check if level is cleared**
            if not bricks:
                level += 1
                ball_speed += 1  # Increase ball speed for the next level

                # **Display "Next Level" message before resetting**
                font = pygame.font.Font(None, 74)
                next_level_text = font.render(f"Level {level}", True, GREEN)
                screen.fill(WHITE)
                screen.blit(next_level_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  # Pause for 2 seconds before restarting

                break  # Exit inner loop to restart the level

            # **Ball out of bounds (Game Over)**
            if ball.rect.bottom >= SCREEN_HEIGHT:
                if not show_retry_popup():
                    pygame.quit()
                    exit()
                else:
                    break  # Restart the level if retry

            # Draw everything
            paddle.draw()
            ball.draw()
            for brick in bricks:
                brick.draw()

            # **Display Level**
            font = pygame.font.Font(None, 50)
            level_text = font.render(f"Level: {level}", True, BLACK)
            screen.blit(level_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)



if __name__ == "__main__":
    main()