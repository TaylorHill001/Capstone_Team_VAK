import pygame
from Breakout import *
from settings import *
from pygame.locals import *



#Menu fuctionality 

#Main Menu
#Looks for any key press to start game. 
def show_main_menu():
    font = pygame.font.Font(None, 50)
    text = font.render("Breakout Game", True, "blue")
    subtext = font.render("Press any key to continue", True, "green")

    while True:
       
        screen.fill("black")
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
    text = font.render("Game Paused", True, "red")
    subtext = font.render("Press any key to resume", True, "white")

    while True:
        screen.fill("black")
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
        screen.fill("black")  # Clear screen
        text = font.render(str(counter), True, "white")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)  # Draw countdown
        
        pygame.display.flip()  # Update screen
        pygame.time.delay(1000)  # Wait 1 second
        counter -= 1  # Decrease counter

    screen.fill("black")  # Clear the countdown after finishing
    pygame.display.flip()



#Scoring Menu
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Scores")

# Load font
font = pygame.font.Font(None, 50)

def draw_scores():
    """Renders and displays the scores on the screen."""
    screen.fill("black")  

    title_text = font.render("Top Scores", True, "white")
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    subtext = font.render("Press any key to continue", True, "green")
    screen.blit(title_text, title_rect)
    screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 1.4))

    #This is score parsing from the .txt file functionality. 
    high_scores = []
    try:
        with open(HIGH_SCORES_FILE, "r") as file:
            data = file.read().strip()
            users = data.split(",")

            for users in users:
                parts = users.strip().split(" ")
                if len(parts) == 3:  # Was getting a length unpack error ,this will check it.
                    name, score, level = parts
                    high_scores.append((name.strip(), score.strip(), level.strip()))
    except FileNotFoundError:
        print(f"Error: {HIGH_SCORES_FILE} not found!")


    while True:

        # Draw scores
        for i, (name, score, level) in enumerate(high_scores):
            score_text = font.render(f"{i+1}. {name}: {score} (Lvl {level})", True, "blue")
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180 + i * 50))
            screen.blit(score_text, score_rect)

        pygame.display.flip()  

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    return 
