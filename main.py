import pygame
import sys
import Vector

# Initialize Pygame
pygame.init()

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

FONT = pygame.font.SysFont(None, 36)

# Button settings
button_width, button_height = 150, 60
button_margin = 20
button_color_default = (30, 30, 30)
button_color_hover = (80, 80, 80)
button_color_held = (255, 0, 0)
button_outline_color = BULLET_HIT_COLOUR

button_rect = pygame.Rect(
    WIDTH - button_width - button_margin,
    HEIGHT - button_height - button_margin,
    button_width,
    button_height,
)
def ShootGun():
    # This function calculates where the bullet will be fired based on previous bullet location and recoil timers
    return

def drawBulletHit(x, y):
    thickness = 0 if FILL_CIRCLE else 1
    pygame.draw.circle(screen, BULLET_HIT_COLOUR, (int(x), int(y)), BULLET_RADIUS, thickness)
    return

def drawLineFromPoints(lx, ly, rx, ry):
    return


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(60) / 1000  # Frame time in seconds (not used yet)
    width, height = screen.get_size()
    # Determine button color
    if button_rect.collidepoint(mouse_pos):
        if mouse_pressed[0]:
            color = button_color_held
            ShootGun()
        else:
            color = button_color_hover
    else:
        color = button_color_default

        # Fill screen with dark gray
    screen.fill((30, 30, 30))
    # drawBulletHit(width//2, height//2)
    # Draw button fill
    pygame.draw.rect(screen, color, button_rect)

    # Draw button outline
    pygame.draw.rect(screen, button_outline_color, button_rect, 3)

    # Render and draw text centered on button
    text_surf = FONT.render("SHOOT", True, BULLET_HIT_COLOUR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    # Flip display
    pygame.display.flip()
    clock.tick(120)

