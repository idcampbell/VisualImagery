from os.path import join
from random import randint, sample
from glob import glob
from PIL import Image
from psychopy import core, prefs, visual, sound
import librosa
#prefs.hardware['audioLib'] = ['PTB']

# Load the stimuli
face_img_paths = sorted(glob('Stimuli/Images/People/*'))
face_audio_paths = sorted(glob('Stimuli/Audio/People/*.wav'))
letter_img_paths = sorted(glob('Stimuli/Images/Letters/*'))
letter_audio_paths = sorted(glob('Stimuli/Audio/Letters/*.wav'))

face_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in face_img_paths}
letter_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in letter_img_paths}
face_audio = {path.split('/')[-1].split('.wav')[0].replace('_', ' '): path for path in face_audio_paths}
letter_audio = {path.split('/')[-1].split('.mp3')[0].replace('_', ' '): librosa.load(path) for path in letter_audio_paths}

def run_miniblock(img_stimuli, audio_stimuli, window, n_stimuli=4, stim_len=4.0, cond='open'):
    # Display/play the miniblock cue.
    if cond=='open':
        message = visual.TextStim(window, text='Open your eyes')
        #### TODO: PLAY AUDIO OF CUE ####
    else:
        message = visual.TextStim(window, text='Close your eyes')
        #### TODO: PLAY AUDIO OF CUE ####
    message.draw()
    window.flip()
    core.wait(stim_len)

    # Present the stimuli for the miniblock.
    stim_keys = list(img_stimuli.keys())
    block_stims = sample(stim_keys, n_stimuli)
    for stim in block_stims:
        # Prepare the stimulus text.
        txt_stim = visual.TextStim(window, text=stim, pos=(0.0, 0.8))
        txt_stim.draw()
        # Prepare the image stimulus.
        img_stim = visual.ImageStim(window, image=img_stimuli[stim])
        img_stim.size = (1.2, 1.4) # NOTE: this looks approximately right to me, but may need to be adjusted.
        img_stim.draw()
        # Prepare the audio stimulus.
        #audio_vec = audio_stimuli[stim][0].reshape(-1,1)
        #sr = audio_stimuli[stim][1]
        #print(audio_vec.shape)
        #print(sr)
        #audio_data = sound.AudioClip(audio_vec, sampleRateHz=sr)
        #print(audio_data._checkCodecSupported('mp3'))
        #audio_data = audio_stimuli[stim]
        #audio_stim = sound.Sound(audio_data, sampleRate=22050)
        #flip_hook = window.getFutureFlipTime(clock='ptb')
        #audio_stim.play(when=flip_hook)
        # Present the whole stimulus.
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

win = run_miniblock(face_imgs, face_audio, win, n_stimuli=4, stim_len=1.0, cond='open')

# Clean things up.
win.close()
core.quit()
