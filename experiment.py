from glob import glob
from os.path import join
from PIL import Image

import os
os.environ['DISPLAY'] = ':1'

# Load the stimuli
face_img_paths = sorted(glob('Stimuli/Images/People/*'))
face_audio_paths = sorted(glob('Stimuli/Audio/People/*'))
letter_img_paths = sorted(glob('Stimuli/Images/Letters/*'))
letter_audio_paths = sorted(glob('Stimuli/Audio/Letters/*'))
face_imgs = [Image.open(img) for img in face_img_paths]
letter_imgs = [Image.open(img) for img in letter_img_paths]

# Set up the experiment
from psychopy import core, visual
 
# Create a window
win = visual.Window([400,300])
 
# Create a stimulus for a certain window
message = visual.TextStim(win, text="Hello World!")

