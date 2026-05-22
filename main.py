import os
import sys
import random
import math
import pygame

#GET THE CORRECT DIRECTORY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 2
COIN_VALUE = 10
STARTING_LIVES = 3
COINS_TO_WIN = 15
INVINCIBLE_FRAMES = 45

#INITIALIZATION
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Quest: The Last Coin")
clock = pygame.time.Clock()

font_small = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 48)
font_large = pygame.font.Font(None, 72)

#ASSET HELPERS
def load_image(path, size=None, fallback_color=(255, 0, 255)):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        surface = pygame.Surface(size if size else (40, 40), pygame.SRCALPHA)
        surface.fill(fallback_color)
        return surface

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

def load_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.4)
        return True
    except pygame.error:
        return False
    
# ASSETS
player_frames = [
    load_image(os.path.join(IMAGE_DIR, "player_walk1.png"), (40, 40), fallback_color=(50, 200, 255)),
    load_image(os.path.join(IMAGE_DIR, "player_walk2.png"), (40, 40), fallback_color=(50, 220, 255)),
    load_image(os.path.join(IMAGE_DIR, "player_walk3.png"), (40, 40), fallback_color=(50, 240, 255)),
]

enemy_img = load_image(os.path.join(IMAGE_DIR, "enemy.png"), (35, 35), fallback_color=(255, 80, 80))
coin_img = load_image(os.path.join(IMAGE_DIR, "coin.png"), (20, 20), fallback_color=(255, 215, 0))
background_img = load_image(os.path.join(IMAGE_DIR, "background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(20, 20, 60))

collect_sound = load_sound(os.path.join(SOUND_DIR, "collect.wav"))
hurt_sound = load_sound(os.path.join(SOUND_DIR, "hurt.wav"))
victory_sound = load_sound(os.path.join(SOUND_DIR, "victory.wav"))

load_music(os.path.join(BASE_DIR, "background.mp3"))

# SPRITE CLASSES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = player_frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image = self.frames[0].copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = PLAYER_SPEED
        self.invincible_timer = 0

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            alpha = 128 if self.invincible_timer % 6 < 3 else 255
        else:
            alpha = 255

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            moving = True

        if moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = 0

        center = self.rect.center
        current_surface = self.frames[self.current_frame].copy()
        current_surface.set_alpha(alpha)
        self.image = current_surface
        self.rect = self.image.get_rect(center=center)
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def hit(self):
        if self.invincible_timer == 0:
            self.invincible_timer = INVINCIBLE_FRAMES
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = ENEMY_SPEED * random.choice([-1, 1])
        self.speed_y = ENEMY_SPEED * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(30, SCREEN_HEIGHT - 30)
        self.start_y = self.rect.y
        self.bob_offset = random.randint(0, 100)

    def update(self):
        self.rect.y = self.start_y + int(math.sin(pygame.time.get_ticks() * 0.004 + self.bob_offset) * 3)


# HELPER FUNCTIONS
def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))

def reset_game():
    player = Player()
    enemies = pygame.sprite.Group(
        *[Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(3)]
    )
    coins = pygame.sprite.Group(Coin() for _ in range(12))
    all_sprites = pygame.sprite.Group(player, *enemies, *coins)

    return {
        "player": player,
        "enemies": enemies,
        "coins": coins,
        "all_sprites": all_sprites,
        "score": 0,
        "lives": STARTING_LIVES,
        "game_over": False,
        "game_win": False,
    }

# MAIN GAME LOOP
def main():
    state = reset_game()
    if load_music(os.path.join(BASE_DIR, "background.mp3")):
        pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (state["game_over"] or state["game_win"]) and event.key == pygame.K_SPACE:
                    state = reset_game()
                    if load_music(os.path.join(BASE_DIR, "background.mp3")):
                        pygame.mixer.music.play(-1)

        if not state["game_over"] and not state["game_win"]:
            state["player"].update()
            state["enemies"].update()
            state["coins"].update()

            collected = pygame.sprite.spritecollide(state["player"], state["coins"], dokill=True)
            for _ in collected:
                state["score"] += COIN_VALUE
                if collect_sound:
                    collect_sound.play()
                new_coin = Coin()
                state["coins"].add(new_coin)
                state["all_sprites"].add(new_coin)

            if pygame.sprite.spritecollide(state["player"], state["enemies"], dokill=False):
                if state["player"].hit():
                    state["lives"] -= 1
                    if hurt_sound:
                        hurt_sound.play()
                    state["player"].rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    for enemy in state["enemies"]:
                        enemy.rect.x = random.randint(0, SCREEN_WIDTH - 35)
                        enemy.rect.y = random.randint(0, SCREEN_HEIGHT - 35)

            if state["score"] >= COINS_TO_WIN * COIN_VALUE:
                state["game_win"] = True
                if victory_sound:
                    victory_sound.play()
                pygame.mixer.music.stop()

            if state["lives"] <= 0:
                state["game_over"] = True
                pygame.mixer.music.stop()

        screen.blit(background_img, (0, 0))
        state["all_sprites"].draw(screen)

        draw_text(f"Score: {state['score']}", font_small, (255, 255, 255), 10, 10)
        draw_text(f"Lives: {state['lives']}", font_small, (255, 255, 255), 10, 45)
        coins_left = max(0, (COINS_TO_WIN * COIN_VALUE - state["score"]) // COIN_VALUE)
        draw_text(f"Coins left: {coins_left}", font_small, (255, 255, 255), 10, 80)

        if state["game_over"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            draw_text("GAME OVER", font_large, (255, 50, 50), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, center=True)
            draw_text(f"Final Score: {state['score']}", font_medium, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            draw_text("Press SPACE to play again", font_small, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, center=True)

        if state["game_win"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            draw_text("YOU WIN!", font_large, (50, 255, 50), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, center=True)
            draw_text(f"Final Score: {state['score']}", font_medium, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            draw_text("You collected all the coins!", font_medium, (255, 255, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
            draw_text("Press SPACE to play again", font_small, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120, center=True)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()