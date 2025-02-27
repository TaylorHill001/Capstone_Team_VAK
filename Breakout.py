import pygame
from pygame.locals import *
from settings import *
from paddle import Paddle
from ball import Ball
from brick import create_bricks
from scores import Scores
from menus import *

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Arcade Game")
clock = pygame.time.Clock()
running = True

# Display retry popup
def show_retry_popup():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over! Try Again?", True, "red")
    retry_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    yes_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 100, 50)
    no_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 90, 50)

    while running:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text, retry_rect)

        pygame.draw.rect(screen, "green", yes_button)
        pygame.draw.rect(screen, "red", no_button)

        yes_text = font.render("Yes", True, "white")
        no_text = font.render("No", True, "white")

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

def show_name_popup():
    font = pygame.font.Font(None, 74)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 350, 50)
    text = ""
    error_message = ""
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        congrats_text = font.render("High Score Reached!!!", True, TEXT_COLOR)
        screen.blit(congrats_text, (SCREEN_WIDTH // 2 - 270, SCREEN_HEIGHT // 2 - 160))
        prompt = font.render("Please Enter Your Name: ", True, TEXT_COLOR)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 60))

        # Draw input box
        pygame.draw.rect(screen, BACKGROUND_COLOR, input_box, 2)
        txt_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        if error_message:
            error = font.render(error_message, True, "red")
            screen.blit(error, ((SCREEN_WIDTH - error.get_width()) // 2, SCREEN_HEIGHT // 2 + 60))
                   
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if text == '':
                        error_message = "Enter a name"
                    elif " " in text:
                        error_message = "No spaces allowed in name"
                    elif "," in text:
                        error_message = "No commas allowed in name"
                    else:
                        return text  # Return entered name when Enter is pressed
                elif event.key == K_BACKSPACE:
                    text = text[:-1]  # Remove last character
                else:
                    text += event.unicode  # Add typed character

# Main game loop
def main():
    #Main menu only appears at start of the game. 
    # Will not show again after level pass or restart. 
    show_main_menu() 
    draw_scores() #Scores show up before each game begins
    scores = Scores()
    level = 1
    ball_speed = 4

    while True:
        menu_timer() #Count down timer gives players time to prepare to play. 
        paddle = Paddle()
        ball = Ball(ball_speed)
        bricks = create_bricks()

        while running:
            screen.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        pause_menu()

            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("LEFT")
            if keys[pygame.K_RIGHT]:
                paddle.move("RIGHT")

            ball.move()

            # Ball collision with paddle (adjust angle based on impact position)
            if ball.rect.colliderect(paddle.rect):
                offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)
                ball.dy = -ball.speed
                ball.dx = ball.speed * offset  # Adjust angle based on impact position

            # Ball collision with bricks
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    score = brick.get_brick_score(level)
                    scores.increase_score(score)
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
                next_level_text = font.render(f"Level {level}", True, "green")
                screen.fill(BACKGROUND_COLOR)
                screen.blit(next_level_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  # Pause for 2 seconds before restarting

                break  # Exit inner loop to restart the level

            # **Ball out of bounds (Game Over)**
            if ball.rect.bottom >= SCREEN_HEIGHT:
                if scores.compare_current_score() is not None:
                    player_name = show_name_popup()
                    scores.update_high_scores(player_name, level)
                scores.reset_score()
                draw_scores() #Scores show up before each game begins
                if not show_retry_popup():
                    pygame.quit()
                    exit()
                else:
                    break  # Restart the level if retry

            # Draw everything
            paddle.draw(screen)
            ball.draw(screen)
            for brick in bricks:
                brick.draw(screen)
            font = pygame.font.Font(None, 50)
            level_text = font.render(f"Level: {level}", True, TEXT_COLOR)
            screen.blit(level_text, (320, 15))
            score_text = font.render(f"Score: {scores.current_score}", True, TEXT_COLOR)
            screen.blit(score_text, (20, 15))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()