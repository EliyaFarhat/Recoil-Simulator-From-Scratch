from Vector import *
from Button import *
from WeaponRecoil import *
# Initialize Pygame
pygame.init()
# more concurrent sounds
pygame.mixer.set_num_channels(32)
# Window settings
WIDTH, HEIGHT = 800, 700
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

OFFSETS = {
    "X" : 0,
    "Y" : 0,
    "Z" : 0,
}




# Now we need to define variables that will control the recoil pattern
# We need a timer that will keep track of the time since last fired and if the gun is fired again while this timer is still active, recoil will be applied without the buildup
# We need a limiter to the recoil and some variables to control how far left and right the bullets land
# We need counters to ensure that the gun does not fire tooooo many bullets to the left or right
# We need a max side offset, the bullet will never fire futher than a specified distance
CENTER_AXIS = Custom_Vector(0,0,1)

list_of_bullets = []

FONT = pygame.font.SysFont(None, 36)

# Button settings
button_width, button_height = 150, 60
button_margin = 20
button_color_default = (30, 30, 30)
button_color_hover = (80, 80, 80)
button_color_held = (54, 14, 14)
button_outline_color = BULLET_HIT_COLOUR

Weapons = {
    "Vandal" : {
        "Ammo" : 50,
        "fireRate" : 9.75,
        "timeToReachMaxRecoil": 1.5,
        "maxRecoilAngle" : 1.00,
        "firstShotError": 0.25,
        "maxYOffset" : 0.05,
        "recoilDecayRate" : 3,
        "Name": "Vandal",
        "maxTiltOffset" : 0.015,
    },
    "Phantom": {
        "Ammo": 50,
        "fireRate": 11,
        "timeToReachMaxRecoil": 2,
        "maxRecoilAngle": 1.00,
        "firstShotError": 0.2,
        "maxYOffset": 0.05,
        "recoilDecayRate": 1.5,
        "Name": "Vandal",
        "maxTiltOffset": 0.015,
    },
}


currentWeapon = Weapons["Vandal"]

MAX_RECOIL_RESET_TIME = 1 # second

TARGET_DISTANCE = 2800 # units away

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


def draw_recoil_progress_bar(surface, x, y, width, height, progress, bg_color=(50, 50, 50), fg_color=(232, 131, 0)):

    # Draw background
    pygame.draw.rect(surface, bg_color, (x, y, width, height))

    # Calculate filled height based on progress (fill from bottom up)
    fill_height = int(height * progress)

    # Draw filled rect
    pygame.draw.rect(surface, fg_color, (x, y + height - fill_height, width, fill_height))

    # Optional: draw border
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2)

def FindIntersection(randomVector, distanceOfPlane):
    t = distanceOfPlane/randomVector.z
    tx, ty, tz = randomVector.x * t, randomVector.y * t, t*randomVector.z
    return Custom_Vector(tx, ty, tz)
def ShootGun():
    # This function calculates where the bullet will be fired based on previous bullet location and recoil timers
    SHOOT_SOUND.play()

    angle, offset, tilt_offset, progress = weaponRecoil.shoot()

    randomVector = random_vector_in_cone(angle, currentWeapon["firstShotError"], progress, currentWeapon["maxYOffset"]) # modify this to add previous bullet dependence
    intersection = FindIntersection(randomVector, TARGET_DISTANCE)
    # Transform intersection for pygame
    screen_x = width // 2 + intersection.x
    screen_y = (height // 2 - intersection.y)  #- offset
    # Check if point is within screen bounds
    if 0 <= screen_x < width and 0 <= screen_y < height:
        AddBullet(screen_x, screen_y, list_of_bullets)
        drawBulletHit(screen_x, screen_y)

def drawBulletHit(x, y):
    thickness = 0 if FILL_CIRCLE else 1
    pygame.draw.circle(screen, BULLET_HIT_COLOUR, (int(x), int(y)), BULLET_RADIUS, thickness)
    return

def drawLineFromPoints(lx, ly, rx, ry):
    return

time_since_last_bullet = 0
weaponRecoil = WeaponRecoil(currentWeapon["timeToReachMaxRecoil"],
                            currentWeapon["firstShotError"],
                            currentWeapon["maxRecoilAngle"],
                            currentWeapon["maxYOffset"],
                            currentWeapon["recoilDecayRate"],
                            currentWeapon["maxTiltOffset"])
def ClearScreen(bullets):
    bullets.clear()

def AddBullet(x, y, bullets):
    if len(bullets) == currentWeapon["Ammo"]:
        bullets.pop(0)  # remove the oldest bullet (front of the list)
    bullets.append((x, y))
def LoadBullets(bullets):
    for x, y in bullets:
        drawBulletHit(x, y)



running = True
lastBulletHeight = None
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    dt = clock.tick(120) / 1000
    width, height = screen.get_size()
    FIRE_RATE = currentWeapon["fireRate"]
    screen.fill((30, 30, 30))
    pygame.draw.circle(screen, (59, 65, 74), (int(width // 2), int(height // 2)), 300, 1)
    pygame.draw.circle(screen, (59, 65, 74), (int(width//2), int(height//2)), 200, 1)
    pygame.draw.circle(screen, (59, 65, 74), (int(width//2), int(height//2)), 80, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if clear_button.is_clicked(event):
            ClearScreen(list_of_bullets)
            print("CLEARING CANVAS")


    recoil_progress = weaponRecoil.GetProgress()
    # Define bar dimensions and position (right side)
    bar_width = 20
    bar_height = 200
    bar_x = WIDTH - bar_width - 10  # 10 px from right edge
    bar_y = (HEIGHT - bar_height) // 2  # vertically centered

    # Draw the progress bar
    draw_recoil_progress_bar(screen, bar_x, bar_y, bar_width, bar_height, recoil_progress)
    LoadBullets(list_of_bullets)
    # Update buttons
    shoot_button.update(mouse_pos, mouse_pressed)
    clear_button.update(mouse_pos, mouse_pressed)
    currTime = pygame.time.get_ticks()

    if (shoot_button.is_held and (time_since_last_bullet == 0 or currTime - time_since_last_bullet >= (1000/FIRE_RATE))):
        # Do something while SHOOT is being held
        time_since_last_bullet = currTime

        ShootGun()
    else:
        if not shoot_button.is_held:
            weaponRecoil.update()

    # Draw scene

    shoot_button.draw(screen)
    clear_button.draw(screen)

    pygame.display.flip()
    clock.tick(120)

