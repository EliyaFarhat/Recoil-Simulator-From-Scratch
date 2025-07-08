from Vector import *
from Button import *
from WeaponRecoil import *
from Weapons import Weapons
import pygame
import time

# Initialize Pygame
pygame.init()
pygame.mixer.set_num_channels(32)

# Window settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recoil Simulator")
clock = pygame.time.Clock()

# Bullet settings
BULLET_HIT_COLOUR = (232, 131, 0)
BULLET_RADIUS = 8
LINE_COLOUR = (232, 131, 0)
LINE_THICKNESS = 2
FILL_CIRCLE = False
SHOW_LINES = True

CENTER_AXIS = Custom_Vector(0, 0, 1)
list_of_bullets = []
FONT = pygame.font.SysFont(None, 36)

# UI button styling
button_width, button_height = 150, 60
button_margin = 20
button_color_default = (30, 30, 30)
button_color_hover = (80, 80, 80)
button_color_held = (54, 14, 14)
button_outline_color = BULLET_HIT_COLOUR

# Weapons & Default
weapon_names = list(Weapons.keys())
current_weapon_index = 0
currentWeapon = Weapons[weapon_names[current_weapon_index]]

weaponRecoil = WeaponRecoil(currentWeapon["timeToReachMaxRecoil"],
                            currentWeapon["firstShotError"],
                            currentWeapon["maxRecoilAngle"],
                            currentWeapon["maxYOffset"],
                            currentWeapon["recoilDecayRate"],
                            currentWeapon["maxTiltOffset"])

def SwitchWeapon(index):
    global currentWeapon
    currentWeapon = Weapons[weapon_names[index]]
    weaponRecoil.ChangeWeapon(currentWeapon)

# Buttons
shoot_button = Button(WIDTH - button_width - button_margin,
                      HEIGHT - button_height - button_margin,
                      button_width,
                      button_height,
                      "SHOOT",
                      FONT,
                      button_color_default,
                      button_color_hover,
                      button_color_held,
                      button_outline_color)

clear_button = Button(button_margin,
                      HEIGHT - button_height - button_margin,
                      button_width,
                      button_height,
                      "CLEAR",
                      FONT,
                      button_color_default,
                      button_color_hover,
                      button_color_held,
                      button_outline_color)

prev_weapon_button = Button(button_margin,
                            button_margin,
                            60, 50,
                            "<",
                            FONT,
                            button_color_default,
                            button_color_hover,
                            button_color_held,
                            button_outline_color)

next_weapon_button = Button(WIDTH - 60 - button_margin,
                            button_margin,
                            60, 50,
                            ">",
                            FONT,
                            button_color_default,
                            button_color_hover,
                            button_color_held,
                            button_outline_color)

SHOOT_SOUND = pygame.mixer.Sound("SFX/ShotSFX.mp3")
TARGET_DISTANCE = 2500
MAX_RECOIL_RESET_TIME = 1

def draw_recoil_progress_bar(surface, x, y, width, height, progress,
                              bg_color=(50, 50, 50), fg_color=(232, 131, 0)):
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    fill_height = int(height * progress)
    pygame.draw.rect(surface, fg_color, (x, y + height - fill_height, width, fill_height))
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2)

def FindIntersection(randomVector, distanceOfPlane):
    t = distanceOfPlane / randomVector.z
    return Custom_Vector(randomVector.x * t, randomVector.y * t, randomVector.z * t)

def ShootGun():
    SHOOT_SOUND.play()
    angle, offset, tilt_offset, progress = weaponRecoil.shoot()
    randomVector = random_vector_in_cone(angle, currentWeapon["firstShotError"], progress, currentWeapon["maxYOffset"])
    intersection = FindIntersection(randomVector, TARGET_DISTANCE)
    screen_x = WIDTH // 2 + intersection.x
    screen_y = HEIGHT // 2 - intersection.y

    # Compute distance from screen center
    dx = screen_x - WIDTH // 2
    dy = screen_y - HEIGHT // 2
    distance_from_center = (dx ** 2 + dy ** 2) ** 0.5

    if distance_from_center <= 300:
        AddBullet(screen_x, screen_y, list_of_bullets)
        drawBulletHit(screen_x, screen_y)

def drawBulletHit(x, y):
    pygame.draw.circle(screen, BULLET_HIT_COLOUR, (int(x), int(y)), BULLET_RADIUS, 0 if FILL_CIRCLE else 1)

def AddBullet(x, y, bullets):
    if len(bullets) == currentWeapon["Ammo"]:
        bullets.pop(0)
    bullets.append((x, y))

def LoadBullets(bullets):
    for x, y in bullets:
        drawBulletHit(x, y)

def ClearScreen(bullets):
    bullets.clear()

time_since_last_bullet = 0
running = True
lastBulletHeight = None

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    dt = clock.tick(120) / 1000
    width, height = screen.get_size()
    FIRE_RATE = currentWeapon["fireRate"]

    screen.fill((30, 30, 30))
    pygame.draw.circle(screen, (59, 65, 74), (WIDTH // 2, HEIGHT // 2), 300, 2)
    pygame.draw.circle(screen, (59, 65, 74), (WIDTH // 2, HEIGHT // 2), 200, 2)
    pygame.draw.circle(screen, (59, 65, 74), (WIDTH // 2, HEIGHT // 2), 80, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if clear_button.is_clicked(event):
            ClearScreen(list_of_bullets)

        # Weapon switching
        if prev_weapon_button.is_clicked(event):
            ClearScreen(list_of_bullets)
            current_weapon_index = (current_weapon_index - 1) % len(weapon_names)
            SwitchWeapon(current_weapon_index)
        if next_weapon_button.is_clicked(event):
            ClearScreen(list_of_bullets)
            current_weapon_index = (current_weapon_index + 1) % len(weapon_names)
            SwitchWeapon(current_weapon_index)

    # Update
    shoot_button.update(mouse_pos, mouse_pressed)
    clear_button.update(mouse_pos, mouse_pressed)
    prev_weapon_button.update(mouse_pos, mouse_pressed)
    next_weapon_button.update(mouse_pos, mouse_pressed)

    # Fire weapon logic
    currTime = pygame.time.get_ticks()
    if shoot_button.is_held and (time_since_last_bullet == 0 or currTime - time_since_last_bullet >= (1000 / FIRE_RATE)):
        time_since_last_bullet = currTime
        ShootGun()
    elif not shoot_button.is_held:
        weaponRecoil.update()

    # Draw progress bar
    recoil_progress = weaponRecoil.GetProgress()
    draw_recoil_progress_bar(screen, WIDTH - 30, (HEIGHT - 200) // 2, 20, 200, recoil_progress)

    # Draw bullets
    LoadBullets(list_of_bullets)

    # Draw current weapon name
    weapon_text = FONT.render(weapon_names[current_weapon_index], True, (220, 220, 220))
    text_rect = weapon_text.get_rect(center=(WIDTH // 2, button_margin + 25))
    screen.blit(weapon_text, text_rect)

    # Draw UI buttons
    shoot_button.draw(screen)
    clear_button.draw(screen)
    prev_weapon_button.draw(screen)
    next_weapon_button.draw(screen)

    pygame.display.flip()
    clock.tick(120)
