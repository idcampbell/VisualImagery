import os
from os.path import join
from random import randint, sample
from glob import glob
from PIL import Image
from psychopy import core, visual
import librosa
#os.environ['DISPLAY'] = ':1'

# Load the stimuli
face_img_paths = sorted(glob('Stimuli/Images/People/*'))
face_audio_paths = sorted(glob('Stimuli/Audio/People/*'))
letter_img_paths = sorted(glob('Stimuli/Images/Letters/*'))
letter_audio_paths = sorted(glob('Stimuli/Audio/Letters/*'))

face_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in face_img_paths}
letter_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in letter_img_paths}
face_audio = {path.split('/')[-1].split('.mp3')[0].replace('_', ' '): librosa.load(path) for path in face_audio_paths}
letter_audio = {path.split('/')[-1].split('.mp3')[0].replace('_', ' '): librosa.load(path) for path in letter_audio_paths}

def run_miniblock(stimuli, window, n_stimuli=4, stim_len=4.0, cond='open'):
    # Play the miniblock cue.
    if cond=='open':
        message = visual.TextStim(window, text='Open your eyes')
        #### TODO: PLAY AUDIO OF CUE ####
    else:
        message = visual.TextStim(window, text='Close your eyes')
        #### TODO: PLAY AUDIO OF CUE ####
    message.draw()
    window.flip()
    core.wait(stim_len)
    # Display the stimuli for the miniblock.
    stim_keys = list(stimuli.keys())
    block_stims = sample(stim_keys, n_stimuli)
    for stim in block_stims:
        print(stim)
        txt_stim = visual.TextStim(window, text=stim)
        img_stim = visual.ImageStim(window, image=stimuli[stim])
        txt_stim.draw()
        img_stim.draw()
        window.flip()
        core.wait(stim_len)
    return window


# Create a window
win = visual.Window([400,300])
 
# Create a stimulus for a certain window
#message = visual.TextStim(win, text="Hello World!")
#message.draw()
#win.flip()
#core.wait(5.0)

win = run_miniblock(face_imgs, win, n_stimuli=4, stim_len=1.0, cond='open')

# Clean things up.
win.close()
core.quit()
