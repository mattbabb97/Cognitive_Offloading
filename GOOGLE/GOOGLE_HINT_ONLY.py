#______ ___________  _____  ___________   _   _ _____ _   _ _____ 
#|  ___|  _  | ___ \/  __ \|  ___|  _  \ | | | |_   _| \ | |_   _|
#| |_  | | | | |_/ /| /  \/| |__ | | | | | |_| | | | |  \| | | |  
#|  _| | | | |    / | |    |  __|| | | | |  _  | | | | . ` | | |  
#| |   \ \_/ / |\ \ | \__/\| |___| |/ /  | | | |_| |_| |\  | | |  
#\_|    \___/\_| \_| \____/\____/|___/   \_| |_/\___/\_| \_/ \_/  

# CODE BY MATTHEW H. BABB ALL RIGHTS RESERVED !!!!!!!!!!!!
# Do NOT use this code without the permission of original author !!!!!!!!!!!!
                                                                                                                                
import sys                  # Import the 'system' library
import random               # Import the 'random' library which gives cool functions for randomizing numbers
from random import choice
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions
import Matts_Toolbox        # Import Matt's Toolbox with LRC specific functions

pygame.init()               # This initializes all pygame modules

# READ TECHNICAL FILES ------------------------------------------------------------------------------------------------

# Grab the monkey name from monkey.txt
with open("monkey.txt") as f:
    monkey = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

# ----------------------------------------------------------------------------------------------------------------------

"""SET UP LOCAL VARIABLES --------------------------------------------------------------------------------------------"""

white = (255, 255, 255)                                         # This sets up colors you might need
blue = (200, 120, 200)
black = (0, 0, 0)                                               # Format is (Red, Green, Blue, Alpha)
green = (0, 200, 0)                                             # 0 is the minimum 260 is the maximum
red = (250, 0, 0)                                               # Alpha is the transparency of a color
transparent = (0, 0, 0, 0)

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("Incorrect.wav")           # This sets your incorrect sound
sound_sparkle = pygame.mixer.Sound("sparkle.wav")

"""Put your Screen Parameters here"""
scrSize = (800, 600)                                            # Standard Resolution of Monkey Computers is 800 x 600
scrRect = pygame.Rect((0, 0), scrSize)                          # Sets the shape of the screen to be a rectangle
fps = 60                                                        # Frames Per Second


"""FILE MANIPULATION FUNCTIONS --------------------------------------------------------------------------------------"""

# Create an Output File
from Matts_Toolbox import writeLn

# Name the file of your Data Output
from Matts_Toolbox import makeFileName

# Get parameters from parameters.txt
from Matts_Toolbox import getParams

# Save parameters into their own file for safe keeping
from Matts_Toolbox import saveParams

"""SCREEN MANIPULATION FUNCTIONS ------------------------------------------------------------------------------------"""
from Matts_Toolbox import setScreen

from Matts_Toolbox import refresh

        # Argument to pass: Surface

"""HELPER FUNCTIONS -------------------------------------------------------------------------------------------------"""
# Quit Program Function
from Matts_Toolbox import quitEscQ

# Sound Playing Function
from Matts_Toolbox import sound

# Pellet Dispensing Function
from Matts_Toolbox import pellet

# Moving the Cursor
from Matts_Toolbox import joyCount
from Matts_Toolbox import moveCursor

from Matts_Toolbox import pseudorandomize
from Matts_Toolbox import shuffle_array

"""LIST OF TODOS ----------------------------------------------------------------------------------------------------"""

# TODO: Work on writing data into excel file
# TODO: Check to make sure training parameters work
# TODO: Delete excess/unused code
# TODO: Remove print() statements for seconds

"""ICON CLASS -------------------------------------------------------------------------------------------------------"""

from Matts_Toolbox import Box

# Draws the Icons for Ephemeral and Permanent buttons
class Icon(Box):
    def __init__(self, PNG, position, scale):                                  # Pass the image and position (x,y)
        super(Icon, self).__init__()
        image = pygame.image.load(PNG).convert_alpha()                          # image = image you passed in arguments
        self.size = image.get_size()                                            # Get the size of the image
        self.image = pygame.transform.smoothscale(image, scale)                 # Scale the image = scale inputted
        self.rect = self.image.get_rect()                                       # Get rectangle around the image
        self.rect.center = self.position = position                             # Set rectangle and center at position
        self.mask = pygame.mask.from_surface(self.image)                        # Creates a mask object

    def mv2pos(self, position):                                           # Move the Image obj to position (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position = position


"""TRIAL CLASS -----------------------------------------------------------------------------------------------------"""

class Trial(object):
    def __init__(self):
        super(Trial, self).__init__()
        self.train_or_test = train_or_test                  # Determine if this is a Training or a Testing Phase
        self.trial_number = 0                               # Trial Number {1 - 80}
        self.trial_within_block = -1                        # Trial Within the current block {0 - 9}
        self.block = 1                                      # Block number {1-20}
        self.block_length = trials_per_block                # Number of trials per block = stored in parameters.txt
        self.blocks_per_session = blocks_per_session        # Number of blocks per session stored in parameters.txt
        self.start_time = 0
        
        self.startphase = True                              # start button
        self.phase1 = False                                 # Phase 1: Target Flashes for 5 sec
        self.phase2 = False                                 # Phase 2: Blank Screen
        self.phase3 = False                                 # Phase 3: Hint button pops up, if clicked go back to Phase 1
        self.phase4 = False                                 # Phase 4: 4 Stimuli pop up
        self.phase5 = False
        self.phase6 = False
        
        self.stimID = -1                                     # stimID used to indicate which stimuli flashes
        self.stimuli_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        random.shuffle(self.stimuli_idx)

        self.trial_type = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]


        if self.train_or_test == 1:
            self.trial_type = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]        # Trial Type = 2: Hint Trial

        elif self.train_or_test == 2:
            self.trial_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]        # Trial Type = 3: Probe (Fake Hint Trial)


        # Keep Track of Whether a Hint was used
        # Automatically set to False
        self.hint_used = False

        # Keep Track of Training Performance
        self.correct_pct = 0.00 
        self.num_correct = 0
        self.consecutive = 0

        self.targets = glob.glob('stimuli/*.png')
        
        self.stimuli = []                                                           # Create a blank list for stimuli input
        self.icon_position = [(150,150), (650,450), (150, 450), (650, 150)]         # Create a list for the four Positions
        random.shuffle(self.icon_position)

        self.delay_interval = [5, 10, 5, 5, 5, 10, 5, 10, 5, 10, 5, 10, 5, 10, 5, 5, 5, 10, 10, 10, 5, 10, 10, 10]
        #self.delay_interval = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        random.shuffle(self.delay_interval)
        self.target_timer = 4.000   # The length of time the stimuli is presented for learning
        self.hint_timer = 5.000     # The length of time the hint is available for selection

    def new(self):
        global start_time
        global subselection
        global SELECT
        SELECT = -1
        self.trial_number += 1                                                # Increment trial number by 1
        self.trial_within_block += 1                                          # Increment trial within block by 1
        self.stimID += 1
        #sound_chime.play()
        print("Trial: " + str(self.trial_number))
        print("Trial_within_block: " + str(self.trial_within_block))
        print("Block: " + str(self.block))
        print("Trial Type: " + str(self.trial_type))


        if self.trial_within_block == (self.block_length / 2):
            self.stimID = -1
            #random.shuffle(self.stimuli_idx)

        if self.trial_within_block == self.block_length:                      # If this is the last trial in the block
            self.trial_within_block = 0                                       # Reset this to 0           
            self.newBlock()                                                   # Run .newBlock()
            print("Block Complete!")

        self.hint_used = False
        self.startphase = True
        self.phase1 = False
        self.phase2 = False
        self.phase3 = False
        self.phase4 = False
        self.phase6 = False

        random.shuffle(self.icon_position)                              # Randomise the stimuli positions
        self.create_stimuli()                                           # Run .create_stimuli()
        cursor.mv2pos((400, 550))                                       # Move the cursor to the start position
        #self.start_time = pygame.time.get_ticks()


    def newBlock(self):
        """Moves program to the next block and randomizes the trial types"""
        self.stimID = -1
        self.block += 1                                                 # Increment block by 1
        random.shuffle(self.stimuli_idx)
        self.hint_used = False

        if self.block > self.blocks_per_session:                             # Check if this is the last block in the session
            print("Session Complete!")                                          # If it is, then quit!
            pygame.quit()
            sys.exit()

    def create_stimuli(self):
        """Create the stimuli based on the trial type"""
        """By using choice() we will select icons with stimID that are not equal to the target stimID"""
        global icon_condition

        Icons = [Icon("start.png", (150, 200), (140, 140)),
                 Icon(self.targets[self.stimuli_idx[self.stimID]], (0, 0), (200, 200)),
                 Icon(self.targets[self.stimuli_idx[choice([i for i in range(0, 3) if i not in [self.stimID]])]], (0, 0), (200, 200)),
                 Icon(self.targets[self.stimuli_idx[choice([i for i in range(4, 7) if i not in [self.stimID]])]], (0, 0), (200, 200)),
                 Icon(self.targets[self.stimuli_idx[choice([i for i in range(8, 11) if i not in [self.stimID]])]], (0, 0), (200, 200)),
                 Icon("hint.png", (400, 500), (800, 800))
                ]

        self.stimuli = [Icons[0], Icons[1], Icons[2], Icons[3], Icons[4], Icons[5]]
        # 0 = Start Button # 1 = Correct MTS # 2 = Distractor # 3 = Distractor # 4 = Distractor # 5 = Hint Button
           


    def draw_start(self):
        """Draw the start button at center of the screen"""
        self.stimuli[0].mv2pos((400, 400))
        self.stimuli[0].draw(screen)

    def draw_target(self):
        """Draw the target at the center of the screen"""
        if self.trial_type[self.trial_within_block] == 1:
            screen.fill(white)
        elif self.trial_type[self.trial_within_block] == 2:
            screen.fill(blue)
        self.stimuli[1].mv2pos((400, 150))
        self.stimuli[1].draw(screen)
        #cursor.draw(screen)
        #moveCursor(cursor)
        if self.time_delay() >= 4:
            self.phase1 = False
            self.phase2 = True

    def draw_target_hint(self):
        """Draw the target at the center of the screen"""
        screen.fill(blue)
        #cursor.draw(screen)
        #moveCursor(cursor)
        self.stimuli[1].mv2pos((400, 150))
        self.stimuli[1].draw(screen)

        if self.time_delay()- self.current_timer >= 3:
            cursor.mv2pos((400, 300))
            self.phase4 = False
            self.phase6 = True

    def pre_trial_delay(self):
        """Present a blank screen for standardized 2 sec prior to the presentation of all 4 choice options"""
        if self.trial_type[self.trial_within_block] == 1:
            screen.fill(white)
        elif self.trial_type[self.trial_within_block] == 2:
            screen.fill(blue)
            cursor.draw(screen)
            moveCursor(cursor)
        if self.time_delay()- self.total_delay >= 2:
            cursor.mv2pos((400, 300))
            self.phase5 = False
            self.phase6 = True

    def draw_hint_button(self):
        #sound_sparkle.play()
        self.stimuli[5].mv2pos((400, 250))
        self.stimuli[5].draw(screen)

    def draw_stimuli(self):
        """Draw the stimuli at their positions after start button is selected"""
        global icon_positions
        self.stimuli[1].mv2pos(self.icon_position[0])
        self.stimuli[1].draw(screen)
        self.stimuli[2].mv2pos(self.icon_position[1])
        self.stimuli[2].draw(screen)
        self.stimuli[3].mv2pos(self.icon_position[2])
        self.stimuli[3].draw(screen)
        self.stimuli[4].mv2pos(self.icon_position[3])
        self.stimuli[4].draw(screen)

# -----------------------------------------------------------------------------------------------------

    def get_trial_type(self):
        return self.trial_type[self.trial_within_block]
        print("Trial Type: " + str(self.trial_type[self.trial_within_block]))

    def time_delay(self):
        delay_counter = ((pygame.time.get_ticks() - self.start_time)/1000)
        #print(delay_counter)
        return delay_counter


    def trial_duration(self):
        global timer
        global start_time
        global SELECT
        global duration
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)
            #print(seconds)
        if seconds > duration and SELECT != -1:
            seconds = seconds
        elif seconds > duration and SELECT == -1:
            #sound(False)
            start_time = pygame.time.get_ticks()
            self.trial_number -= 1
            self.trial_within_block -= 1
            self.stimID -= 1
            seconds = 0
            selection = 0
            self.startphase = True
            self.new()

        return seconds

    def response_time(self):
        seconds = 0.000
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000.000)

        return seconds
        
    
#----------------------------------------------------------------

    def start(self):
        global SELECT
        global timer
        global start_time
        if self.trial_type[self.trial_within_block] == 1:
            screen.fill(white)
        elif self.trial_type[self.trial_within_block] == 2:
            screen.fill(blue)
            
        # self.total_delay = interval time + target_timer
        if self.delay_interval[self.trial_within_block] == 5:
            self.total_delay = 9.000
        elif self.delay_interval[self.trial_within_block] == 10:
            self.total_delay = 14.000
        elif self.delay_interval[self.trial_within_block] == 15:
            self.total_delay = 19.000
        elif self.delay_interval[self.trial_within_block] == 20:
            self.total_delay = 24.000

        self.draw_start()
        cursor.draw(screen)
        moveCursor(cursor, only = 'up')

        if cursor.collides_with(self.stimuli[0]):
            screen.fill(white)
            self.start_time = pygame.time.get_ticks()
            self.startphase = False
            self.draw_target()
            self.phase1 = True
# Phase 2
    def blank_screen(self):
        if self.trial_type[self.trial_within_block] == 1:
            screen.fill(white)
        elif self.trial_type[self.trial_within_block] == 2:
            screen.fill(blue)
            cursor.mv2pos((400, 300))
        #cursor.draw(screen)
        #moveCursor(cursor)
        if self.trial_type[self.trial_within_block] == 1:                                                           # If this is a standard trial
            if self.time_delay() - self.target_timer >= self.delay_interval[self.trial_within_block]:               # and if the time delay - 4.0 sec becomes greater than the delay_interval
                self.phase2 = False                                                                                 # The blank screen goes away, and advance to phase 3
                self.phase3 = True
        elif self.trial_type[self.trial_within_block] == 2:                                                                 # If this is a hint trial
            if self.time_delay() - self.target_timer >= self.delay_interval[self.trial_within_block] - self.hint_timer:     # and the time delay - 4.0 sec becomes greater than delay_inteval - the hint_timer
                self.phase2 = False                                                                                         # the hint button appears advancing to phase 3
                self.runtime_timer = self.time_delay()
                print(self.runtime_timer)
                self.phase3 = True

# Phase 3
    def run_hint_button(self):
        global SELECT
        if self.trial_type[self.trial_within_block] == 1:                               # If this is a standard trial
            screen.fill(white)                                                          # Just keep the screen blank for the remaining 5 seconds until the toal_delay is reached
            cursor.draw(screen)
            moveCursor(cursor)
            if self.time_delay() >= self.total_delay:
                screen.fill(blue)
                self.pre_trial_delay()
                cursor.mv2pos((400, 300))
                self.phase3 = False
                self.phase5 = True
        elif self.trial_type[self.trial_within_block] == 2:                             # However, if this is a hint trial, ...
            screen.fill(blue)
            self.draw_hint_button()                                                     # Draw the hint button for 5 seconds
            cursor.draw(screen)
            moveCursor(cursor)
            #if self.time_delay() >= self.total_delay:                                   # If the hint button is never selected
                #cursor.mv2pos((400, 300))                                               # Wait 5 seconds, then advance to phase 5 (2 sec pre-presentation delay)
                #self.phase3 = False
                #self.pre_trial_delay()
                #self.phase5 = True

            if cursor.collides_with(self.stimuli[5]):                                   # If the hint button is selected, ...
                screen.fill(blue)                                                       # advance to phase 4 and draw the target stimuli at the top of the screen
                self.hint_used = True
                self.phase3 = False
                self.current_timer = self.time_delay()
                #self.draw_target_hint()
                self.phase4 = True


            if self.time_delay() - self.runtime_timer >= 30:
                sound(False)
                self.write(data_file, 0)
                screen.fill(white)
                refresh(screen)
                pygame.time.delay(time_out * 1000)
                self.new()

            

        

    def run_trial(self):
        global SELECT
        global timer
        global start_time
        global button_positions
        global duration

        if self.trial_type[self.trial_within_block] == 1:
            screen.fill(white)
        elif self.trial_type[self.trial_within_block] == 2:
            screen.fill(blue)
        cursor.draw(screen)
        moveCursor(cursor)
        self.stimuli[0].mv2pos((-50, -50))
        self.stimuli[0].size = 0
        self.stimuli[5].mv2pos((-50, -50))
        self.stimuli[5].size = 0
        self.draw_stimuli()
        #self.trial_duration()
        #self.response_time()

        if self.time_delay() >= self.total_delay + duration + 2:
            sound(False)
            start_time = 0
            self.trial_number -= 1
            self.trial_within_block -= 1
            self.stimID -= 1
            self.phase6 = False
            self.startphase = True
            self.new()

        if SELECT == 1:
            self.write(data_file, 1)
            sound(True)
            pellet()
            self.num_correct += 1
            screen.fill(white)
            refresh(screen)
            pygame.time.delay(ITI * 1000)
            self.new()
        elif SELECT == 2:
            self.write(data_file, 0)
            sound(False)
            screen.fill(white)
            refresh(screen)
            pygame.time.delay(time_out * 1000)
            self.new()
        elif SELECT == 3:
            self.write(data_file, 0)
            sound(False)
            screen.fill(white)
            refresh(screen)
            pygame.time.delay(time_out * 1000)
            self.new()
        elif SELECT == 4:
            self.write(data_file, 0)
            sound(False)
            screen.fill(white)
            refresh(screen)
            pygame.time.delay(time_out * 1000)
            self.new()            
        

    def write(self, file, correct):
        global icon_condition
        now = time.strftime('%H:%M:%S')
        data = [monkey, today, now, self.train_or_test, self.block, self.trial_number, self.trial_type[self.trial_within_block],
                self.delay_interval[self.trial_within_block], self.targets[self.stimuli_idx[self.stimID]],
                self.hint_used,(self.time_delay() - self.total_delay - 2), correct]
        
        writeLn(file, data)



# ---------------------------------------------------------------------------------------------------------------------


# UPLOAD TASK PARAMETERS ----------------------------------------------------------------------------------------------
varNames = ['full_screen', 'train_or_test', 'icon_condition', 'trials_per_block', 'blocks_per_session', 'ITI',
            'duration', 'run_time', 'time_out']
params = getParams(varNames)
globals().update(params)

full_screen = params['full_screen']                     # Since your parameters are stored in a dictionary
train_or_test = params['train_or_test']                       # You can pull their value out with dictionary[key]
icon_condition = params['icon_condition']
trials_per_block = params['trials_per_block']
blocks_per_session = params['blocks_per_session']
ITI = params['ITI']
duration = params['duration']
run_time = params['run_time']
time_out = params['time_out']


# START THE CLOCK
clock = pygame.time.Clock()
start_time = (pygame.time.get_ticks() / 1000)
stop_after = run_time * 60 * 1000

# CREATE THE TASK WINDOW
screen = setScreen(full_screen)
pygame.display.set_caption("Google_Training_Hint_Only")
display_icon = pygame.image.load("Monkey Icon.png")
pygame.display.set_icon(display_icon)
screen.fill(white)

# DEFINE THE CURSOR
cursor = Box(color = red, speed = 8, circle = True)


"""MAKE ICONS FROM PNGs-------------------------------------------------------------------------------------------"""

button_positions = [(175, 300), (625, 300)]                             # Set the LEFT/RIGHT positions for the button icons
icon_positions = [(175, 300), (625, 300)]                               # Set the LEFT/RIGHT positions for the target icons




"""CREATE THE DATA FILE-------------------------------------------------------------------------------------------"""
data_file = makeFileName('NEW_Hint_Only_Training')
writeLn(data_file, ['monkey', 'date', 'time', 'training_or_testing', 'block', 'trial_number', 'trial_type',
                    'delay_interval', 'stimuli_idx', 'hint_used', 'response_time', 'correct_or_incorrect'])



"""SET UP IS COMPLETE - EVERYTHING BELOW THIS IS RUNNING THE MAIN PROGRAM"""


# MAIN GAME LOOP ------------------------------------------------------------------------------------------------------

trial = Trial()             # Initialize a new Trial


trial.new()                 # Begin ;)

running = True
while running:
    quitEscQ()
    timer = (pygame.time.get_ticks() / 1000)
    if timer > run_time:
        pygame.quit()
        sys.exit()
    screen.fill(white)
    cursor.draw(screen)
    
    SELECT = cursor.collides_with_list(trial.stimuli)
    clock.tick(fps)
    
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1 == True:
            trial.draw_target()
        elif trial.phase2 == True:
            trial.blank_screen()
        elif trial.phase3 == True:
            trial.run_hint_button()
        elif trial.phase4 == True:
            trial.draw_target_hint()
        elif trial.phase5 == True:
            trial.pre_trial_delay()
        elif trial.phase6 == True:
            trial.run_trial()




    refresh(screen)

# --------------------------------------------------------------------------------------------------------------------
