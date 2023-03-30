from os.path import join
import argparse
from random import randint, sample
from glob import glob
from PIL import Image
import pandas as pd
from psychopy import core, prefs, visual, sound
from psychopy.hardware import keyboard
from psychopy.hardware.emulator import launchScan
import librosa


def run_block(block_df, img_stimuli, audio_stimuli, window, stim_len=3.0, delay_time=8.0):
    '''Run a block of the experiment (4 miniblocks with 4 experimental conditions each).
        img_stimuli (dict): Contains the loaded images indexed by filepath.
        audio_stimuli (dict): Contains the loaded audio files index by filepath.
        window (psychopy.visual.Window): Experiment display to present the stimuli.
        stim_len (float, optional): Number of seconds to present each stimulus.
        delay_time (float, optional): Length of the delay period presented after each experimental condition.
    '''
    miniblocks = block_df['miniblock'].unique()
    cond_map = {'O': 'open', 'C': 'closed'}
    for im in miniblocks:
        miniblock_df = block_df[block_df.miniblock==im]
        for ic in range(1,4+1):
            # Run the condition.
            cond_df = miniblock_df[miniblock_df.tinyblock==ic]
            cond_images = [img_stimuli[path] for path in cond_df['img_path']]
            cond_audio = [audio_stimuli[path] for path in cond_df['audio_path']]
            eye_cond = cond_map[cond_df.eye_cond.unique()[0]]
            window = run_condition(cond_images, cond_audio, window, stim_len=stim_len, cond=eye_cond)
            # Add a fixation period.
            message = visual.TextStim(window, text='+')
            message.draw()
            window.flip()
            core.wait(delay_time)
    return window


def run_condition(img_stimuli, audio_stimuli, window, stim_len=3.0, cond='open'):
    '''Run a miniblock of the experiment.
            img_stimuli (dict): Contains the loaded images indexed by filepath.
            audio_stimuli (dict): Contains the loaded audio files indexed by filepath.
            window (psychopy.visual.Window): Experiment display to present the stimuli.
            stim_len (float, optional): Number of seconds to present each stimulus.
            cond (str, optional): Experimental condition (e.g. open or closed).
    '''
    # Display/play the miniblock cue.
    message = visual.TextStim(window, text=f'{cond} your eyes')
    message.draw()
    cue_path = f'Stimuli/Audio/{cond}.wav'
    cue_vec, sr = librosa.load(cue_path, sr=48000)
    audio_data = sound.AudioClip(cue_vec.reshape(-1,1))
    audio_stim = sound.Sound(audio_data)
    flip_hook = window.getFutureFlipTime(clock='ptb')
    audio_stim.play(when=flip_hook)
    window.flip()
    core.wait(stim_len)
    # Present the stimuli for the miniblock.
    for img, aud in zip(img_stimuli, audio_stimuli):
        # Prepare the image stimulus.
        img_stim = visual.ImageStim(window, image=img, size=(2.0, 2.0))
        img_stim.draw()
        # Prepare the audio stimulus.
        audio_vec = aud[0].reshape(-1,1)
        audio_data = sound.AudioClip(audio_vec)
        audio_stim = sound.Sound(audio_data)
        flip_hook = window.getFutureFlipTime(clock='ptb')
        audio_stim.play(when=flip_hook)
        # Present the whole stimulus.
        window.flip()
        core.wait(stim_len)
    return window


def parse_args():
    '''Get user arguments for how to run the experiment.
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filepath', type=str, required=True, help='Path to the CSV describing the counterbalanced stimuli for the run.')
    ap.add_argument('-s', '--stimulus_time', type=float, default=3.0, help='Length of time to display each stimulus.')
    ap.add_argument('-d', '--delay_time', type=float, default=6.0, help='Length of time for fixation delay period between miniblocks.')
    args = ap.parse_args()
    return args


if __name__=='__main__':
    # Parse the user arguments.
    args = parse_args()

    # Create a window
    win = visual.Window([400,400])
 
    # Needed to make the audio actually play...
    sound.setDevice(dev=0, kind='output')
    prefs.hardware['audioLib'] = ['ptb']

    # Load the stimuli.
    run_df = pd.read_csv(args.filepath)
    images = {path: Image.open(path) for path in sorted(glob('Stimuli/Images/*/*.jpg'))}
    audio = {path: librosa.load(path, sr=48000) for path in sorted(glob('Stimuli/Audio/*/*.wav'))}

    #### SCANNER SYNCING: May need to get rid of launch scan?? ####
    MR_settings = {'TR': 1.5, 'sync': 'equal', 'volumes': 10.0, 'skip': 0.0}
    launchScan(win, MR_settings, mode='test', wait_msg='Waiting for pulse.')
    key_resp = keyboard.Keyboard()
    while True:
        allKeys = key_resp.getKeys(keyList=['equal'], waitRelease=False)
        if MR_settings['sync'] in allKeys:
            break

    # Run the experiment.
    blocks = run_df['block'].unique()
    for ib in blocks:
        block_df = run_df[run_df.block==ib]
        win = run_block(block_df, images, audio, win, stim_len=args.stimulus_time, delay_time=args.delay_time)
    # Clean things up.
    win.close()
    core.quit()
