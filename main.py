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


def ShootGun():
    # This function calculates where the bullet will be fired based on previous bullet location and recoil timers
    return

def drawBulletHit(x, y):
    thickness = 0 if FILL_CIRCLE else 1
    pygame.draw.circle(screen, BULLET_HIT_COLOUR, (int(x), int(y)), BULLET_RADIUS, thickness)
    return

def drawLineFromPoints(lx, ly, rx, ry):
    return

# Main game loop
while True:
    dt = clock.tick(60) / 1000  # Frame time in seconds (not used yet)
    width, height = screen.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Draw one circle


    # Fill screen with dark gray
    screen.fill((30, 30, 30))
    # drawBulletHit(width//2, height//2)

    # Flip display
    pygame.display.flip()