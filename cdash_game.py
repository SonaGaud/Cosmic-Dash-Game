import pygame
import random
import time
import os

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Dash")

# Load player image
player_image = pygame.image.load("space_rocket.png")
player_image = pygame.transform.scale(player_image, (50, 70))

# Load asteroid image for stars
asteroid_image = pygame.image.load("asteroid_image.png")
asteroid_image = pygame.transform.scale(asteroid_image, (25, 30))

BG = pygame.transform.scale(pygame.image.load("retro.jpg"), (WIDTH, HEIGHT))

PLAYER_VEL = 5
ASTEROID_VEL = 4

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, asteroid, hit, high_score):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "cyan")
    WIN.blit(time_text, (0, 0))

    # Draw player image
    WIN.blit(player_image, (player.x, player.y))

    # Draw asteroid images for stars
    for aste in asteroid:
        WIN.blit(asteroid_image, (aste.x, aste.y))

    if hit:
        lost_text = FONT.render("Game Over! Click to Restart", 6, "yellow")
        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    
    # Display high score
    high_score_text = FONT.render(f"High Score: {round(high_score)}", 1, "magenta")
    WIN.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 0))

def main():
    run = True
    player = pygame.Rect(70, HEIGHT - 70, 50, 70)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    aste_add_increment = 1600
    aste_count = 0

    asteroid = []
    hit = False

    waiting_for_restart = False

    HIGH_SCORE_FILE = "high_score.txt"

    def load_high_score():
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                return float(file.read())
        else:
            return 0

    def save_high_score(score):
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))

    # Load high score at the beginning
    high_score = load_high_score()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hit:
                    # Reset game variables
                    player = pygame.Rect(70, HEIGHT - 70, 50, 70)
                    start_time = time.time()
                    elapsed_time = 0
                    aste_count = 0
                    asteroid = []
                    # Reset star timing mechanism
                    aste_add_increment = 1600
                    hit = False
                    waiting_for_restart = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        if not hit and not waiting_for_restart:
            aste_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if aste_count > aste_add_increment:
                aste_x = random.randint(0, WIDTH - 10)
                aste_y = -20  # Start at the top of the screen
                aste = pygame.Rect(aste_x, aste_y, 10, 20)
                asteroid.append(aste)

                aste_add_increment = max(180, aste_add_increment - 40)
                aste_count = 0

            for aste in asteroid[:]:
                aste.y += ASTEROID_VEL
                if aste.y > HEIGHT:
                    asteroid.remove(aste)
                elif aste.colliderect(player):
                    hit = True
                    waiting_for_restart = True

            # When a new high score is achieved, update and save it
            if elapsed_time > high_score:
                high_score = elapsed_time
                save_high_score(high_score)

        draw(player, elapsed_time, asteroid, hit, high_score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
