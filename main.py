import pygame
import time
import random
import os

pygame.init()
pygame.font.init()

# ====================== SETTINGS ======================
WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Colors
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 100)
YELLOW = (255, 220, 50)
CYAN = (50, 200, 255)
DARK = (10, 10, 30)

# Fonts
FONT = pygame.font.SysFont("comicsans", 32)
BIG_FONT = pygame.font.SysFont("comicsans", 60)
SMALL_FONT = pygame.font.SysFont("comicsans", 24)

HIGHSCORE_FILE = "highscore.txt"

# ====================== LOAD ASSETS ======================
def load_image(name, size=None):
    try:
        img = pygame.image.load(name).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        return None

# ---- Load up to 10 backgrounds ----
BACKGROUNDS = []

# Try real image files first
for i in range(1, 11):
    for ext in [".jpeg", ".jpg", ".png"]:
        img = load_image(f"bg{i}{ext}", (WIDTH, HEIGHT))
        if img:
            BACKGROUNDS.append(img)
            break

# Also try the original single bg.jpeg
original_bg = load_image("bg.jpeg", (WIDTH, HEIGHT))
if original_bg and original_bg not in BACKGROUNDS:
    BACKGROUNDS.append(original_bg)

# ---- Player & Asteroid images ----
SHIP_IMG = load_image("ship.png", (50, 60))

ASTEROID_IMGS = {
    "small": load_image("asteroid1.png", (22, 22)),
    "medium": load_image("asteroid2.png", (34, 34)),
    "big": load_image("asteroid3.png", (52, 52)),
}

# ====================== PROCEDURAL BACKGROUNDS ======================
def create_starfield(variant):
    """Create one of 10 different procedural space backgrounds."""
    surf = pygame.Surface((WIDTH, HEIGHT))

    # Different base colors for variety
    base_colors = [
        (5, 5, 20),      # deep blue-black
        (15, 5, 25),     # purple-ish
        (5, 15, 25),     # teal dark
        (20, 8, 8),      # dark red
        (8, 12, 20),     # navy
        (12, 5, 18),     # violet
        (5, 10, 15),     # green-black
        (18, 10, 5),     # brown-space
        (10, 10, 30),    # classic
        (8, 8, 12),      # almost black
    ]
    surf.fill(base_colors[variant % 10])

    # Stars with different densities and colors
    star_count = 120 + (variant * 15)
    for _ in range(star_count):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        brightness = random.randint(140, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])
        color = (brightness, brightness, brightness)

        # Occasional colored stars
        if random.random() < 0.08:
            color = random.choice([
                (255, 200, 150),  # warm
                (150, 200, 255),  # cool blue
                (255, 150, 200),  # pink
                (200, 255, 150),  # green
            ])

        if size == 1:
            surf.set_at((x, y), color)
        else:
            pygame.draw.circle(surf, color, (x, y), size)

    # Occasional nebula-like soft glow (simple)
    if variant % 3 == 0:
        for _ in range(3):
            cx = random.randint(100, WIDTH - 100)
            cy = random.randint(100, HEIGHT - 100)
            radius = random.randint(80, 180)
            color = random.choice([
                (30, 10, 40), (10, 30, 50), (40, 15, 15), (15, 35, 25)
            ])
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, 40), (radius, radius), radius)
            surf.blit(s, (cx - radius, cy - radius))

    return surf

# If we have fewer than 10 real backgrounds, fill the rest with procedural ones
while len(BACKGROUNDS) < 10:
    BACKGROUNDS.append(create_starfield(len(BACKGROUNDS)))

def get_random_background():
    return random.choice(BACKGROUNDS)

# ====================== HELPER FUNCTIONS ======================
def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    if center:
        rect = surface.get_rect(center=(x, y))
        WIN.blit(surface, rect)
    else:
        WIN.blit(surface, (x, y))

def create_procedural_ship(width=50, height=60):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(surf, CYAN, [
        (width // 2, 0),
        (0, height),
        (width // 2, height - 14),
        (width, height)
    ])
    pygame.draw.polygon(surf, WHITE, [
        (width // 2, 10),
        (width // 2 - 8, height - 18),
        (width // 2 + 8, height - 18)
    ])
    pygame.draw.rect(surf, (255, 100, 50), (width // 2 - 12, height - 8, 8, 8))
    pygame.draw.rect(surf, (255, 100, 50), (width // 2 + 4, height - 8, 8, 8))
    return surf

def create_procedural_asteroid(size, color_variant=0):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    colors = [(170, 170, 170), (140, 130, 120), (190, 160, 130), (120, 120, 130)]
    main_color = colors[color_variant % len(colors)]
    pygame.draw.circle(surf, main_color, (size // 2, size // 2), size // 2)
    for _ in range(random.randint(3, 6)):
        cx = random.randint(4, size - 4)
        cy = random.randint(4, size - 4)
        r = random.randint(2, max(3, size // 6))
        pygame.draw.circle(surf, (60, 60, 60), (cx, cy), r)
    return surf

# ====================== SPRITES ======================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = SHIP_IMG if SHIP_IMG else create_procedural_ship(50, 60)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.vel = 6
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.vel
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, base_speed):
        super().__init__()

        asteroid_type = random.choices(
            ["small", "medium", "big"],
            weights=[0.45, 0.35, 0.20]
        )[0]

        if asteroid_type == "small":
            size = random.randint(18, 26)
            speed_mult = random.uniform(1.4, 1.9)
        elif asteroid_type == "medium":
            size = random.randint(28, 38)
            speed_mult = random.uniform(0.9, 1.2)
        else:
            size = random.randint(45, 60)
            speed_mult = random.uniform(0.55, 0.8)

        self.speed = base_speed * speed_mult

        img = ASTEROID_IMGS.get(asteroid_type)
        if img:
            angle = random.randint(0, 360)
            self.image = pygame.transform.rotate(img, angle)
        else:
            self.image = create_procedural_asteroid(size, random.randint(0, 3))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# ====================== MAIN GAME ======================
def main():
    clock = pygame.time.Clock()
    high_score = load_highscore()

    state = "start"
    score = 0
    start_time = 0
    current_bg = get_random_background()   # random background

    player = Player()
    asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    asteroid_timer = 0
    spawn_delay = 900
    min_spawn_delay = 260
    current_speed = 3.8

    running = True
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == "start" and event.key == pygame.K_SPACE:
                    # Start new game → pick a new random background
                    state = "playing"
                    current_bg = get_random_background()
                    player = Player()
                    asteroids.empty()
                    all_sprites = pygame.sprite.Group(player)
                    score = 0
                    start_time = time.time()
                    asteroid_timer = 0
                    spawn_delay = 900
                    current_speed = 3.8

                elif state == "gameover" and event.key == pygame.K_r:
                    state = "start"
                    current_bg = get_random_background()  # new bg on return to menu too

        # ---------- START SCREEN ----------
        if state == "start":
            WIN.blit(current_bg, (0, 0))
            draw_text("SPACE DODGE", BIG_FONT, CYAN, WIDTH // 2, HEIGHT // 2 - 90, center=True)
            draw_text("Press SPACE to Start", FONT, YELLOW, WIDTH // 2, HEIGHT // 2 + 40, center=True)
            draw_text(f"High Score: {high_score}s", SMALL_FONT, GREEN, WIDTH // 2, HEIGHT // 2 + 90, center=True)
            draw_text("\"Left Arrow\" \"Right Arrow\" or  A D  to move", SMALL_FONT, WHITE, WIDTH // 2, HEIGHT - 50, center=True)
            pygame.display.update()
            continue

        # ---------- PLAYING ----------
        if state == "playing":
            elapsed = time.time() - start_time
            score = int(elapsed)

            asteroid_timer += dt
            if asteroid_timer >= spawn_delay:
                asteroid_timer = 0
                for _ in range(random.randint(1, 3)):
                    a = Asteroid(current_speed)
                    asteroids.add(a)
                    all_sprites.add(a)

                spawn_delay = max(min_spawn_delay, spawn_delay - 11)
                current_speed = min(8.5, current_speed + 0.035)

            player.update(keys)
            asteroids.update()

            hits = pygame.sprite.spritecollide(player, asteroids, True)
            if hits:
                player.lives -= 1
                if player.lives <= 0:
                    state = "gameover"
                    if score > high_score:
                        high_score = score
                        save_highscore(high_score)

            WIN.blit(current_bg, (0, 0))
            all_sprites.draw(WIN)

            draw_text(f"Time: {score}s", FONT, WHITE, 15, 12)
            lives_color = RED if player.lives == 1 else GREEN
            draw_text(f"Lives: {player.lives}", FONT, lives_color, 15, 50)
            draw_text(f"Best: {high_score}s", SMALL_FONT, YELLOW, WIDTH - 160, 15)

            pygame.display.update()

        # ---------- GAME OVER ----------
        if state == "gameover":
            WIN.blit(current_bg, (0, 0))
            draw_text("GAME OVER", BIG_FONT, RED, WIDTH // 2, HEIGHT // 2 - 90, center=True)
            draw_text(f"You survived {score} seconds", FONT, WHITE, WIDTH // 2, HEIGHT // 2 - 15, center=True)

            if score >= high_score and score > 0:
                draw_text("NEW HIGH SCORE!", FONT, YELLOW, WIDTH // 2, HEIGHT // 2 + 35, center=True)
            else:
                draw_text(f"High Score: {high_score}s", FONT, GREEN, WIDTH // 2, HEIGHT // 2 + 35, center=True)

            draw_text("Press R to Restart", FONT, CYAN, WIDTH // 2, HEIGHT // 2 + 100, center=True)
            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()