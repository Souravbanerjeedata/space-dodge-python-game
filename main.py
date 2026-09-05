import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, 'red', player)
    pygame.display.update()

def main():
    run = True
    player  = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0

    stars = []

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        draw(player, elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()