import os

import pygame
import sys
from Vector import *
from Button import *
# Initialize Pygame
pygame.init()
# more concurrent sounds
pygame.mixer.set_num_channels(32)
# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recoil Simulator")

# Clock for controlling frame rate
clock = pygame.time.Clock()


# Player distance from wall
# Bullet and graphics/colour info
BULLET_HIT_COLOUR = (232, 131, 0)
BULLET_RADIUS = 8
LINE_COLOUR = (232, 131, 0)
LINE_THICKNESS = 2
FILL_CIRCLE = False
SHOW_LINES = True

# Gun
AMMO = 25
FIRE_RATE = 9.75 # RDS/SEC
FIRST_SHOT_SPREAD = 0.25 # DEG

BULLET_LIMIT = 50 # bullets on the screen at a time

# Now we need to define variables that will control the recoil pattern
# We need a timer that will keep track of the time since last fired and if the gun is fired again while this timer is still active, recoil will be applied without the buildup
# We need a limiter to the recoil and some variables to control how far left and right the bullets land
# We need counters to ensure that the gun does not fire tooooo many bullets to the left or right
# We need a max side offset, the bullet will never fire futher than a specified distance
CENTER_AXIS = Custom_Vector(0,0,1)

FONT = pygame.font.SysFont(None, 36)

# Button settings
button_width, button_height = 150, 60
button_margin = 20
button_color_default = (30, 30, 30)
button_color_hover = (80, 80, 80)
button_color_held = (255, 0, 0)
button_outline_color = BULLET_HIT_COLOUR

MAX_RECOIL_RESET_TIME = 1 # second

# Create buttons
shoot_button = Button(
    WIDTH - button_width - button_margin,
    HEIGHT - button_height - button_margin,
    button_width,
    button_height,
    "SHOOT",
    FONT,
    button_color_default,
    button_color_hover,
    button_color_held,
    button_outline_color
)

clear_button = Button(
    button_margin,
    HEIGHT - button_height - button_margin,
    button_width,
    button_height,
    "CLEAR",
    FONT,
    button_color_default,
    button_color_hover,
    button_color_held,
    button_outline_color
)
SHOOT_SOUND = pygame.mixer.Sound("SFX/ShotSFX.mp3")
def ShootGun():
    # This function calculates where the bullet will be fired based on previous bullet location and recoil timers
    SHOOT_SOUND.play()
    return

def drawBulletHit(x, y):
    thickness = 0 if FILL_CIRCLE else 1
    pygame.draw.circle(screen, BULLET_HIT_COLOUR, (int(x), int(y)), BULLET_RADIUS, thickness)
    return

def drawLineFromPoints(lx, ly, rx, ry):
    return

time_since_last_bullet = 0

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    dt = clock.tick(120) / 1000
    width, height = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if clear_button.is_clicked(event):
            print("CLEARING CANVAS")

    # Update buttons
    shoot_button.update(mouse_pos, mouse_pressed)
    clear_button.update(mouse_pos, mouse_pressed)
    currTime = pygame.time.get_ticks()

    if (shoot_button.is_held and (time_since_last_bullet == 0 or currTime - time_since_last_bullet >= (1000/FIRE_RATE))):
        # Do something while SHOOT is being held
        time_since_last_bullet = currTime
        print("SHOT FIRED")
        ShootGun()
    # Draw scene
    screen.fill((30, 30, 30))
    shoot_button.draw(screen)
    clear_button.draw(screen)

    pygame.display.flip()
    clock.tick(120)

