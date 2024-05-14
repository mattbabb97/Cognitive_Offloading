# __    __     __  __     ______        ______   ______     ______     __            ______     ______     __  __
#/\ "-./  \   /\ \_\ \   /\  == \      /\__  _\ /\  __ \   /\  __ \   /\ \          /\  == \   /\  __ \   /\_\_\_\
#\ \ \-./\ \  \ \  __ \  \ \  __<      \/_/\ \/ \ \ \/\ \  \ \ \/\ \  \ \ \____     \ \  __<   \ \ \/\ \  \/_/\_\/_
# \ \_\ \ \_\  \ \_\ \_\  \ \_____\       \ \_\  \ \_____\  \ \_____\  \ \_____\     \ \_____\  \ \_____\   /\_\/\_\
#  \/_/  \/_/   \/_/\/_/   \/_____/        \/_/   \/_____/   \/_____/   \/_____/      \/_____/   \/_____/   \/_/\/_/

import sys
import random
import math
import time
import os
import glob
import pygame
sys.path.append("c:")
sys.path.append("..")


pygame.init()


# READ TECHNICAL FILES ------------------------------------------------------------------------------------------------
# Pellet Dispensing
pelletPath = 'c:\pellet.exe'

# Grab the monkey name from monkey.txt
with open("monkey.txt") as f:
    monkey = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

# ----------------------------------------------------------------------------------------------------------------------
# SET UNIVERSAL VARIABLES  ---------------------------------------------------------------------------------------------
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
transparent = (0, 0, 0, 0)

# SET SCREEN VARIABLES ------------------------------------------------------------------------------------------------
scrSize = (800, 600)
scrRect = pygame.Rect((0, 0), scrSize)
surface = pygame.Surface(scrSize)
surface.fill(white)
fps = 60

sound_correct = pygame.mixer.Sound("correct.wav")
sound_incorrect = pygame.mixer.Sound("incorrect.wav")

# DISPLAY FUNCTIONS----------------------------------------------------------------------------------------------------
def setScreen(full_screen=True, size=scrSize):
    """Define screen with scrSize, no frame, and full screen. Option to set
       full screen = False for window display (for development)."""
    if full_screen:
        return pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(size)


# THIS FUNCTION WILL RESET THE SURFACE AND DRAW A NEW SCREEN
# THIS IS IMPORTANT FOR RESETTING TO THE NEXT TRIAL
def refresh(surface):
    """Blit background to screen and update display."""
    surface.blit(surface, (0, 0))
    pygame.display.update()

# ----------------------------------------------------------------------------------------------
# BOX CLASS -----------------------------------------------------------------------------------------------------------
class Box(pygame.sprite.Sprite):
    def __init__(self, size=(20, 20), position=(400, 300), color=(black), speed=8, circle=False):
        super(Box, self).__init__()
        self.size = size
        self.color = color
        self.speed = speed
        self.circle = circle

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = self.position = position   # self.position and self.rect.center are the same

        # If the image is actually a circle, we set circle = True (Useful for the cursor)
        if self.circle == True:
            self.image.fill(white)
            pygame.draw.ellipse(self.image, self.color, (0, 0, self.size[0], self.size[1]))

        self.mask = pygame.mask.from_surface(self.image)
        # Mask creates a 'mask' object over the Box object basically making transparent parts of the sprite untouchable

    """Methods for Box Class"""
    # Updates box size, color, position, and speed
    def update(self, size=None, color=None, position=None, speed=None):
        self.size = size or self.size
        self.color = color or self.color
        self.position = position or self.position
        self.speed = speed or self.speed

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        if self.circle:
            self.image.fill(white)
            pygame.draw.ellipse(self.image, self.color, (0, 0, self.size[0], self.size[1]))

        self.mask = pygame.mask.from_surface(self.image)

    # Draws the box onto display/screen assigned with setScreen().
    # In this case, set window in setScreen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # Move box x pixels to the right and y pixels down.
    def move(self, x, y):
        self.rect.move_ip(x * self.speed, y * self.speed)
        self.rect.clamp_ip(scrRect)
        self.update(position=self.rect.center)

    # Move box to position (x, y)
    def mv2pos(self, position=None):
        self.update(position=position)

    # Tests for pixel-perfect collision with another Icon (sprite). Return True if contact occurs
    def collides_with(self, sprite):
        offset_x = sprite.rect.left - self.rect.left
        offset_y = sprite.rect.top - self.rect.top
        return self.mask.overlap(sprite.mask, (offset_x, offset_y)) is not None

    # Tests for pixel-perfect collision with an icon on the list
    def collides_with_list(self, list):
        for i, sprite in enumerate(list):
            if self.collides_with(sprite):
                return i                              # Returns the index of the icon if collision is occurring
        return -1                                     # Returns -1 when no collision is occurring

# Moving the Cursor ---------------------------------------------------------------------------------------------------

# SETUP JOYSTICK
joyCount = pygame.joystick.get_count()              # ASKS THE COMPUTER IF THERE IS A JOYSTICK ATTACHED
if joyCount > 0:                                    # IF VALUE > 0 THERE IS ONE ATTACHED
    joy = pygame.joystick.Joystick(0)               # IT WILL TELL YOU THIS IS THE JOYSTICK YOU ARE USING
    joy.init()
    pygame.mouse.set_visible(False)                 # Hides the mouse on the screen

def moveCursor(cursor, only=None, diagonal=True):
    # Move cursor via joystick (if available) or arrow keys (if not).
    # Directions can be constrained by a passing string to `only`.
    # If passing several directions, separate with `, `.
    # Suppress diagonal moves with "diagonal = False".
    # Returns boolean True (False) when cursor is (not) moving.
    # no movement unless kb or joystick input

    x_dir = y_dir = 0                                               # Sets base direction to 0

    # Control the Cursor with Arrow Keys
    key = pygame.key.get_pressed()
    if joyCount == 0:
        if key[pygame.K_LEFT]:
            x_dir = -1
        if key[pygame.K_RIGHT]:
            x_dir = 1
        if key[pygame.K_UP]:
            y_dir = -1
        if key[pygame.K_DOWN]:
            y_dir = 1


    # Control the Cursor with Joystick
    if joyCount > 0:
        x_dir = round(joy.get_axis(0))
        y_dir = round(joy.get_axis(1))

    # Restrict it to Cardinal Directions ONLY
    if not diagonal:
        if x_dir != 0:  y_dir = 0
        if y_dir != 0:  x_dir = 0
    if only:
        # if the argument `only` is specified:
            # get direction constraints as list
            # reset all directions that are not specified
        only = only.split(', ')
        if x_dir < 0 and 'left' not in only:
            x_dir = 0
        if x_dir > 0 and 'right' not in only:
            x_dir = 0
        if y_dir < 0 and 'up' not in only:
            y_dir = 0
        if y_dir > 0 and 'down' not in only:
            y_dir = 0

    cursor.move(x_dir, y_dir)

    if x_dir == y_dir == 0:
        return False
    else:
        return True





# TODO: Sound playing function ----------------------------------------------------------------------------------------

def sound(sound_boolean):               # Pass True to play correct.wav
    if sound_boolean:                   # Pass False to play incorrect.wav
        sound_correct.play()            # TODO: Make it so correct is the only sound ever played
    else:                               # TODO: or remove the sounds entirely
        sound_incorrect.play()

#TODO: Pellet dispensing function -------------------------------------------------------------------------------------
def pellet(num=1):
    for i in range(num):
        if os.path.isfile(pelletPath):
            os.system(pelletPath)
            print(pelletPath)
        else:
            print("pellet")             # Prints pellet is pellet.exe cannot be found
        pygame.time.delay(500)

# TODO: The Quit Escape Function to leave the task
def quitEscQ(file=None):
    """Quit pygame on QUIT, [Esc], and [Q]. Use inside main game loop. Optional
       argument adds blank line to file before exiting."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key in (pygame.K_ESCAPE, pygame.K_q))):
            if file:
                writeLn(file)
            pygame.quit()
            sys.exit()



# FILE MANIPULATION FUNCTIONS -----------------------------------------------------------------------------------------

# TODO: Create an Output File
def writeLn(filename, data='', csv=True):
    """Write a list to a file as comma- or tab-delimited. Not passing a list
       results in a blank line."""
    with open(filename, 'a') as f:
        if csv:
            f.write(','.join(map(str, data)) + '\n')
        else:
            f.write('\t'.join(map(str, data)) + '\n')

#TODO: Name the file of your Data Output
def makeFileName(task='Task', format='csv'):
    """Return string of the form MonkeyName_Task_Date.format."""
    return monkey + '_' + task + '_' + today + '.' + format

#TODO: Get parameters from parameters.txt
def getParams(varNames, filename='parameters.txt'):
    """Read in all even lines from parameters.txt. Takes a list of variable names
       as argument and stores them with their values. Returns a dictionary.
       Encase text values in the parameter file in "", lists in [], etc.!"""
    params = {}
    with open(filename) as txt:
        for i, line in enumerate(txt):
            if i % 2 == 1:
                j = i // 2
                params[varNames[j]] = line.strip('\r\n')
    for key, val in params.items():
        exec('params[key] = %s' % val)
    return params

#TODO: Save parameters into their own file for safe keeping
def saveParams():
    pass

# RANDOMIZATION FUNCTIONS ---------------------------------------------------------------------------------------------

def pseudorandomize(array):
    random.shuffle(array)
    new_array = array
    i = 2
    while i <= len(new_array) - 1:
        if new_array[i] == new_array[i - 1] and new_array[i - 2]:
            random.shuffle(new_array)
            i = 2
        i += 1
    return new_array

def shuffle_array(array):
    random.shuffle(array)
    new_array = array
    return new_array

