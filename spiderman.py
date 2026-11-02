
import pygame
import random
import math

# ============================================================
# MARVEL: COLLISION COURSE
# A 2D superhero action adventure
# ============================================================

pygame.init()

WIDTH = 1200
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MARVEL: COLLISION COURSE")

clock = pygame.time.Clock()

# -------------------- COLOURS --------------------

BLACK = (10, 13, 24)
WHITE = (245, 245, 245)
RED = (210, 35, 55)
BLUE = (45, 100, 210)
GOLD = (255, 190, 65)
ORANGE = (255, 125, 40)
PURPLE = (135, 85, 220)
CYAN = (80, 200, 230)
DARK_BLUE = (18, 32, 62)
GREY = (100, 110, 130)
GREEN = (80, 190, 125)

# -------------------- FONTS --------------------

FONT = pygame.font.SysFont("Arial", 20, bold=True)
SMALL = pygame.font.SysFont("Arial", 15, bold=True)
TITLE = pygame.font.SysFont("Arial", 65, bold=True)
SUBTITLE = pygame.font.SysFont("Arial", 29, bold=True)

# -------------------- GAME STATES --------------------

MENU = "menu"
SELECT = "select"
GAME = "game"
PAUSED = "paused"
WON = "won"
LOST = "lost"

game_state = MENU

# -------------------- GAME VARIABLES --------------------

selected_character = 0

score = 0
health = 100
camera_x = 0

level_width = 4000

game_time = 0

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def draw_text(text, font, colour, x, y, center=False):
    image = font.render(str(text), True, colour)

    if center:
        rect = image.get_rect(center=(x, y))
    else:
        rect = image.get_rect(topleft=(x, y))

    screen.blit(image, rect)


def draw_button(text, rect, colour, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)

    current_colour = (
        tuple(min(255, c + 35) for c in colour)
        if hovered else colour
    )

    pygame.draw.rect(
        screen, current_colour, rect,
        border_radius=9
    )

    pygame.draw.rect(
        screen, WHITE, rect,
        2, border_radius=9
    )

    draw_text(
        text, FONT, WHITE,
        rect.centerx, rect.centery,
        center=True
    )

    return hovered


def draw_background():
    # Sky gradient
    for y in range(HEIGHT):
        t = y / HEIGHT

        colour = (
            int(16 + 35 * t),
            int(25 + 24 * t),
            int(55 + 35 * t)
        )

        pygame.draw.line(
            screen, colour,
            (0, y), (WIDTH, y)
        )

    # Moon
    pygame.draw.circle(
        screen, (215, 220, 225),
        (950, 135), 43
    )

    pygame.draw.circle(
        screen, (190, 200, 220),
        (950, 135), 43, 2
    )

    # Distant skyline
    for i in range(24):
        x = (i * 70 - camera_x * 0.2) % (WIDTH + 100)
        height = 110 + (i * 37 % 170)

        pygame.draw.rect(
            screen, (25, 35, 60),
            (int(x), 430 - height, 65, height + 320)
        )

        for wy in range(440 - height + 15, 430, 28):
            pygame.draw.rect(
                screen, (110, 120, 150),
                (int(x) + 12, wy, 5, 9)
            )

    # Foreground skyline
    for i in range(14):
        x = (i * 115 - camera_x * 0.4) % (WIDTH + 150)
        height = 190 + (i * 53 % 180)

        pygame.draw.rect(
            screen, (17, 27, 47),
            (int(x), 500 - height, 105, height + 250)
        )

        for wx in range(int(x) + 12, int(x) + 95, 24):
            for wy in range(500 - height + 15, 500, 35):
                pygame.draw.rect(
                    screen,
                    random.choice([
                        (190, 155, 95),
                        (110, 145, 185),
                        (65, 95, 135)
                    ]),
                    (wx, wy, 7, 12)
                )


# ============================================================
# CHARACTER CLASS
# ============================================================

class Player:

    def __init__(self, character):

        self.character = character

        self.x = 100
        self.y = 480

        self.width = 38
        self.height = 65

        self.vx = 0
        self.vy = 0

        self.speed = 5
        self.jump_power = 14

        self.on_ground = False

        self.facing = 1

        self.attack_cooldown = 0
        self.ability_cooldown = 0

        self.invincible = 0

        self.animation = 0

    def colour(self):

        if self.character == 0:
            return RED

        if self.character == 1:
            return GOLD

        return PURPLE

    def move(self, keys):

        self.vx = 0

        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.facing = -1

        if keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.facing = 1

        if self.on_ground and (
            keys[pygame.K_UP] or keys[pygame.K_w]
        ):
            self.vy = -self.jump_power
            self.on_ground = False

        self.x += self.vx

        self.vy += 0.65

        if self.vy > 15:
            self.vy = 15

        self.y += self.vy

        self.animation += 0.15

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        if self.invincible > 0:
            self.invincible -= 1

    def rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def attack(self):

        if self.attack_cooldown > 0:
            return None

        self.attack_cooldown = 25

        if self.character == 0:
            # Spider-Man web attack
            return pygame.Rect(
                self.x + self.width if self.facing == 1
                else self.x - 100,
                self.y + 15,
                100,
                28
            )

        if self.character == 1:
            # Iron Man repulsor attack
            return pygame.Rect(
                self.x + self.width if self.facing == 1
                else self.x - 130,
                self.y + 10,
                130,
                45
            )

        # Doctor Strange magical attack
        return pygame.Rect(
            self.x + self.width if self.facing == 1
            else self.x - 110,
            self.y - 5,
            110,
            85
        )

    def special_ability(self):

        if self.ability_cooldown > 0:
            return False

        self.ability_cooldown = 150

        if self.character == 0:
            # Spider-Man web dash
            self.vx = self.facing * 15
            self.vy = -5

        elif self.character == 1:
            # Iron Man flight burst
            self.vy = -15
            self.vx = self.facing * 10

        else:
            # Doctor Strange magical leap
            self.vy = -18
            self.vx = self.facing * 5

        return True

    def draw(self, camera):

        sx = int(self.x - camera)
        sy = int(self.y)

        if self.invincible > 0 and self.invincible % 6 < 3:
            return

        colour = self.colour()

        # Character shadow
        pygame.draw.ellipse(
            screen, (5, 9, 19),
            (sx - 5, sy + 59, 48, 10)
        )

        # Legs
        pygame.draw.rect(
            screen, DARK_BLUE,
            (sx + 7, sy + 37, 10, 25),
            border_radius=4
        )

        pygame.draw.rect(
            screen, DARK_BLUE,
            (sx + 22, sy + 37, 10, 25),
            border_radius=4
        )

        # Boots
        pygame.draw.rect(
            screen, colour,
            (sx + 3, sy + 57, 17, 8),
            border_radius=3
        )

        pygame.draw.rect(
            screen, colour,
            (sx + 19, sy + 57, 17, 8),
            border_radius=3
        )

        # Torso
        pygame.draw.rect(
            screen, colour,
            (sx + 4, sy + 17, 30, 30),
            border_radius=8
        )

        # Suit centre
        pygame.draw.rect(
            screen, DARK_BLUE,
            (sx + 13, sy + 20, 12, 23),
            border_radius=4
        )

        # Arms
        pygame.draw.line(
            screen, colour,
            (sx + 7, sy + 23),
            (sx + 1, sy + 43), 8
        )

        pygame.draw.line(
            screen, colour,
            (sx + 31, sy + 23),
            (sx + 37, sy + 43), 8
        )

        # Head
        pygame.draw.ellipse(
            screen, colour,
            (sx + 5, sy - 3, 28, 25)
        )

        # Character-specific details
        if self.character == 0:

            # Spider-Man mask lenses
            pygame.draw.ellipse(
                screen, WHITE,
                (sx + 8, sy + 5, 9, 6)
            )

            pygame.draw.ellipse(
                screen, WHITE,
                (sx + 21, sy + 5, 9, 6)
            )

            # Spider emblem
            pygame.draw.circle(
                screen, WHITE,
                (sx + 19, sy + 29), 3
            )

            pygame.draw.line(
                screen, WHITE,
                (sx + 19, sy + 31),
                (sx + 19, sy + 39), 2
            )

        elif self.character == 1:

            # Iron Man faceplate
            pygame.draw.rect(
                screen, (255, 220, 120),
                (sx + 9, sy + 5, 20, 12),
                border_radius=3
            )

            pygame.draw.line(
                screen, CYAN,
                (sx + 10, sy + 9),
                (sx + 28, sy + 9), 2
            )

            # Arc reactor
            pygame.draw.circle(
                screen, CYAN,
                (sx + 19, sy + 31), 6
            )

            pygame.draw.circle(
                screen, WHITE,
                (sx + 19, sy + 31), 2
            )

        else:

            # Doctor Strange
            pygame.draw.rect(
                screen, (190, 35, 45),
                (sx - 3, sy + 19, 44, 8),
                border_radius=3
            )

            pygame.draw.circle(
                screen, GOLD,
                (sx + 19, sy + 30), 5
            )

            # Eye details
            pygame.draw.circle(
                screen, WHITE,
                (sx + 12, sy + 8), 2
            )

            pygame.draw.circle(
                screen, WHITE,
                (sx + 26, sy + 8), 2
            )


# ============================================================
# ENEMIES
# ============================================================

class Enemy:

    def __init__(self, x, platform_y):

        self.x = x
        self.y = platform_y - 48

        self.start_x = x

        self.direction = 1
        self.speed = 1.5

        self.alive = True

    def rect(self):

        return pygame.Rect(
            int(self.x), int(self.y), 35, 48
        )

    def update(self):

        self.x += self.direction * self.speed

        if self.x > self.start_x + 90:
            self.direction = -1

        if self.x < self.start_x - 90:
            self.direction = 1

    def draw(self, camera):

        if not self.alive:
            return

        x = int(self.x - camera)
        y = int(self.y)

        pygame.draw.rect(
            screen, (75, 83, 105),
            (x + 4, y + 10, 27, 35),
            border_radius=6
        )

        pygame.draw.circle(
            screen, (110, 120, 140),
            (x + 17, y + 10), 12
        )

        pygame.draw.circle(
            screen, RED, (x + 12, y + 9), 3
        )

        pygame.draw.circle(
            screen, RED, (x + 22, y + 9), 3
        )

        pygame.draw.line(
            screen, BLACK,
            (x + 8, y + 45),
            (x + 5, y + 48), 4
        )

        pygame.draw.line(
            screen, BLACK,
            (x + 26, y + 45),
            (x + 30, y + 48), 4
        )


# ============================================================
# LEVEL DESIGN
# ============================================================

platforms = [
    pygame.Rect(0, 590, 700, 160),
    pygame.Rect(760, 530, 380, 220),
    pygame.Rect(1200, 590, 420, 160),
    pygame.Rect(1700, 510, 400, 240),
    pygame.Rect(2200, 570, 430, 180),
    pygame.Rect(2750, 490, 420, 260),
    pygame.Rect(3300, 570, 700, 180),

    pygame.Rect(300, 480, 130, 20),
    pygame.Rect(880, 410, 130, 20),
    pygame.Rect(1370, 470, 150, 20),
    pygame.Rect(1820, 390, 140, 20),
    pygame.Rect(2350, 450, 150, 20),
    pygame.Rect(2900, 365, 150, 20),
]

def draw_platforms():

    for p in platforms:

        x = int(p.x - camera_x)

        if x + p.width < 0 or x > WIDTH:
            continue

        pygame.draw.rect(
            screen, (32, 43, 63),
            (x, p.y, p.width, p.height)
        )

        pygame.draw.rect(
            screen, (100, 125, 155),
            (x, p.y, p.width, 5)
        )

        # Rooftop details
        for i in range(x + 15, x + p.width - 10, 60):
            pygame.draw.line(
                screen, (55, 69, 91),
                (i, p.y + 12),
                (i + 25, p.y + 12), 2
            )


# ============================================================
# COLLECTIBLES
# ============================================================

collectibles = [
    pygame.Rect(x, y, 25, 25)
    for x, y in [
        (330, 430),
        (910, 360),
        (1450, 420),
        (1880, 340),
        (2400, 400),
        (2950, 315),
        (3450, 520)
    ]
]

collected = []


def draw_collectibles():

    for i, item in enumerate(collectibles):

        if i in collected:
            continue

        x = int(item.x - camera_x)
        y = item.y + math.sin(game_time * 0.06 + i) * 5

        if -30 < x < WIDTH + 30:

            pygame.draw.circle(
                screen, (80, 60, 35),
                (x + 12, int(y) + 12), 17
            )

            pygame.draw.circle(
                screen, GOLD,
                (x + 12, int(y) + 12), 11, 3
            )

            pygame.draw.circle(
                screen, WHITE,
                (x + 12, int(y) + 12), 3
            )


# ============================================================
# PORTAL
# ============================================================

portal_rect = pygame.Rect(3780, 410, 90, 180)

def draw_portal():

    x = int(portal_rect.x - camera_x)

    if -150 < x < WIDTH + 150:

        t = game_time * 0.05

        pygame.draw.ellipse(
            screen, (55, 32, 110),
            (x - 20, portal_rect.y - 20, 130, 220)
        )

        pygame.draw.ellipse(
            screen, ORANGE,
            (x, portal_rect.y, 90, 180), 9
        )

        pygame.draw.ellipse(
            screen, GOLD,
            (x + 9, portal_rect.y + 9, 72, 162), 3
        )

        pygame.draw.ellipse(
            screen, (65, 40, 110),
            (x + 15, portal_rect.y + 15, 60, 150)
        )

        # Portal particles
        for i in range(12):

            angle = t + i * math.pi / 6

            px = x + 45 + math.cos(angle) * 48
            py = portal_rect.y + 90 + math.sin(angle) * 88

            pygame.draw.circle(
                screen, GOLD,
                (int(px), int(py)), 3
            )


# ============================================================
# HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen, (10, 16, 30),
        (0, 0, WIDTH, 80)
    )

    pygame.draw.line(
        screen, (110, 130, 160),
        (0, 79), (WIDTH, 79), 2
    )

    names = [
        "SPIDER-MAN",
        "IRON MAN",
        "DOCTOR STRANGE"
    ]

    colours = [RED, GOLD, PURPLE]

    draw_text(
        names[selected_character],
        SUBTITLE, colours[selected_character],
        25, 18
    )

    draw_text(
        "HEALTH", SMALL, WHITE, 370, 15
    )

    pygame.draw.rect(
        screen, (65, 35, 45),
        (370, 40, 200, 16),
        border_radius=5
    )

    pygame.draw.rect(
        screen, GREEN if health > 30 else RED,
        (370, 40, max(0, health * 2), 16),
        border_radius=5
    )

    draw_text(
        f"SCORE: {score}",
        FONT, GOLD, 650, 28
    )

    draw_text(
        "1 / 2 / 3: SWITCH HERO",
        SMALL, WHITE, 830, 15
    )

    draw_text(
        "SPACE: ATTACK",
        SMALL, WHITE, 830, 40
    )

    draw_text(
        "E: SPECIAL ABILITY",
        SMALL, WHITE, 1010, 15
    )

    draw_text(
        "P: PAUSE",
        SMALL, WHITE, 1010, 40
    )


# ============================================================
# CREATE GAME OBJECTS
# ============================================================

player = Player(selected_character)

enemies = [
    Enemy(520, 590),
    Enemy(970, 530),
    Enemy(1480, 590),
    Enemy(1900, 510),
    Enemy(2480, 570),
    Enemy(2990, 490),
    Enemy(3500, 570)
]

attack_effects = []

# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global player, score, health, camera_x
    global collected, enemies, game_state

    player = Player(selected_character)

    score = 0
    health = 100
    camera_x = 0

    collected = []

    enemies = [
        Enemy(520, 590),
        Enemy(970, 530),
        Enemy(1480, 590),
        Enemy(1900, 510),
        Enemy(2480, 570),
        Enemy(2990, 490),
        Enemy(3500, 570)
    ]

    attack_effects.clear()

    game_state = GAME


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    clock.tick(60)

    game_time += 1

    mouse = pygame.mouse.get_pos()

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == GAME:

                if event.key == pygame.K_p:
                    game_state = PAUSED

                if event.key == pygame.K_SPACE:

                    attack = player.attack()

                    if attack:
                        attack_effects.append(
                            [attack, 12]
                        )

                if event.key == pygame.K_e:

                    player.special_ability()

                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3
                ]:

                    selected_character = (
                        event.key - pygame.K_1
                    )

                    player.character = selected_character

                    player.speed = 5
                    player.jump_power = 14

                    if selected_character == 1:
                        player.speed = 5.5

                    if selected_character == 2:
                        player.jump_power = 15

            elif game_state == PAUSED:

                if event.key == pygame.K_p:
                    game_state = GAME

                if event.key == pygame.K_r:
                    reset_game()

            elif game_state in [WON, LOST]:

                if event.key == pygame.K_r:
                    reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == MENU:

                if start_button.collidepoint(mouse):
                    game_state = SELECT

            elif game_state == SELECT:

                if select_buttons[0].collidepoint(mouse):
                    selected_character = 0
                    reset_game()

                elif select_buttons[1].collidepoint(mouse):
                    selected_character = 1
                    reset_game()

                elif select_buttons[2].collidepoint(mouse):
                    selected_character = 2
                    reset_game()

                elif back_button.collidepoint(mouse):
                    game_state = MENU

    # --------------------------------------------------------
    # MENU SCREEN
    # --------------------------------------------------------

    if game_state == MENU:

        camera_x = 0

        draw_background()

        # Dramatic portal
        pulse = 5 * math.sin(game_time * 0.05)

        pygame.draw.ellipse(
            screen, (90, 50, 120),
            (780, 150, 230, 390)
        )

        pygame.draw.ellipse(
            screen, ORANGE,
            (800, 160, 190 + pulse, 370), 8
        )

        pygame.draw.ellipse(
            screen, GOLD,
            (817, 176, 160, 337), 3
        )

        # Title
        draw_text(
            "MARVEL", TITLE, RED,
            95, 160
        )

        draw_text(
            "COLLISION COURSE",
            TITLE, WHITE,
            95, 235
        )

        draw_text(
            "THREE HEROES. THREE POWERS. ONE CRISIS.",
            FONT, GOLD,
            105, 325
        )

        draw_text(
            "A dimensional breach has opened above New York.",
            FONT, WHITE,
            105, 385
        )

        draw_text(
            "The city needs its heroes.",
            FONT, WHITE,
            105, 420
        )

        start_button = pygame.Rect(
            105, 505, 270, 65
        )

        draw_button(
            "START MISSION",
            start_button,
            RED, mouse
        )

        draw_text(
            "CLICK TO BEGIN",
            SMALL, WHITE,
            105, 590
        )

    # --------------------------------------------------------
    # CHARACTER SELECTION
    # --------------------------------------------------------

    elif game_state == SELECT:

        draw_background()

        draw_text(
            "CHOOSE YOUR HERO",
            TITLE, WHITE,
            WIDTH // 2, 115, True
        )

        character_names = [
            "SPIDER-MAN",
            "IRON MAN",
            "DOCTOR STRANGE"
        ]

        descriptions = [
            "WEB DASH",
            "FLIGHT BURST",
            "MAGIC LEAP"
        ]

        character_colours = [
            RED, GOLD, PURPLE
        ]

        select_buttons = []

        for i in range(3):

            x = 115 + i * 365

            rect = pygame.Rect(
                x, 270, 270, 240
            )

            pygame.draw.rect(
                screen, (22, 34, 58),
                rect, border_radius=15
            )

            pygame.draw.rect(
                screen, character_colours[i],
                rect, 3, border_radius=15
            )

            # Character portrait representation
            preview = Player(i)
            preview.x = x + 115
            preview.y = 340
            preview.draw(0)

            draw_text(
                character_names[i],
                SUBTITLE, WHITE,
                x + 135, 435, True
            )

            draw_text(
                descriptions[i],
                SMALL, character_colours[i],
                x + 135, 472, True
            )

            button = pygame.Rect(
                x + 25, 535, 220, 50
            )

            draw_button(
                "SELECT HERO",
                button,
                character_colours[i],
                mouse
            )

            select_buttons.append(button)

        back_button = pygame.Rect(
            35, 35, 125, 45
        )

        draw_button(
            "BACK",
            back_button,
            GREY, mouse
        )

    # --------------------------------------------------------
    # GAMEPLAY
    # --------------------------------------------------------

    elif game_state == GAME:

        keys = pygame.key.get_pressed()

        player.move(keys)

        # Keep player inside level.
        player.x = max(
            0,
            min(player.x, level_width - player.width)
        )

        # Platform collisions.
        player.on_ground = False

        for platform in platforms:

            if player.rect().colliderect(platform):

                if player.vy > 0:

                    if player.y + player.height <= platform.y + 20:

                        player.y = platform.y - player.height
                        player.vy = 0
                        player.on_ground = True

        # Camera movement.
        camera_x = max(
            0,
            min(player.x - WIDTH * 0.4,
                level_width - WIDTH)
        )

        # Background and level.
        draw_background()

        draw_platforms()

        # Enemies.
        for enemy in enemies:

            enemy.update()
            enemy.draw(camera_x)

            if enemy.alive:

                if player.rect().colliderect(enemy.rect()):

                    if player.vy > 2 and player.y + player.height < enemy.y + 25:

                        enemy.alive = False
                        player.vy = -9
                        score += 150

                    elif player.invincible == 0:

                        health -= 15
                        player.invincible = 60

                        player.vx = -player.facing * 5

        # Attacks.
        for effect in attack_effects[:]:

            attack_rect, timer = effect

            attack_screen_rect = attack_rect.copy()
            attack_screen_rect.x -= int(camera_x)

            if selected_character == 0:
                colour = CYAN
            elif selected_character == 1:
                colour = GOLD
            else:
                colour = PURPLE

            pygame.draw.rect(
                screen, colour,
                attack_screen_rect,
                3, border_radius=8
            )

            for enemy in enemies:

                if enemy.alive and attack_rect.colliderect(enemy.rect()):

                    enemy.alive = False
                    score += 150

            effect[1] -= 1

            if effect[1] <= 0:
                attack_effects.remove(effect)

        # Collectibles.
        draw_collectibles()

        for i, item in enumerate(collectibles):

            if i not in collected:

                if player.rect().colliderect(item):

                    collected.append(i)
                    score += 100

        # Portal.
        draw_portal()

        if player.rect().colliderect(portal_rect):

            game_state = WON

        # Player.
        player.draw(camera_x)

        # HUD.
        draw_hud()

        if health <= 0:
            game_state = LOST

        # Instructions.
        draw_text(
            "REACH THE PORTAL!",
            FONT, GOLD, 25, HEIGHT - 45
        )

    # --------------------------------------------------------
    # PAUSE SCREEN
    # --------------------------------------------------------

    elif game_state == PAUSED:

        draw_background()

        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        draw_text(
            "MISSION PAUSED",
            TITLE, WHITE,
            WIDTH // 2, 290, True
        )

        draw_text(
            "Press P to continue",
            FONT, GOLD,
            WIDTH // 2, 385, True
        )

        draw_text(
            "Press R to restart",
            FONT, WHITE,
            WIDTH // 2, 425, True
        )

    # --------------------------------------------------------
    # WIN SCREEN
    # --------------------------------------------------------

    elif game_state == WON:

        draw_background()

        draw_text(
            "MISSION COMPLETE",
            TITLE, GOLD,
            WIDTH // 2, 250, True
        )

        draw_text(
            "NEW YORK HAS BEEN SAVED.",
            SUBTITLE, WHITE,
            WIDTH // 2, 340, True
        )

        draw_text(
            f"FINAL SCORE: {score}",
            FONT, GOLD,
            WIDTH // 2, 410, True
        )

        draw_text(
            "PRESS R TO PLAY AGAIN",
            FONT, WHITE,
            WIDTH // 2, 485, True
        )

    # --------------------------------------------------------
    # GAME OVER SCREEN
    # --------------------------------------------------------

    elif game_state == LOST:

        draw_background()

        draw_text(
            "MISSION FAILED",
            TITLE, RED,
            WIDTH // 2, 270, True
        )

        draw_text(
            "The city still needs its heroes.",
            SUBTITLE, WHITE,
            WIDTH // 2, 355, True
        )

        draw_text(
            f"FINAL SCORE: {score}",
            FONT, GOLD,
            WIDTH // 2, 420, True
        )

        draw_text(
            "PRESS R TO TRY AGAIN",
            FONT, WHITE,
            WIDTH // 2, 490, True
        )

    pygame.display.flip()

pygame.quit()
