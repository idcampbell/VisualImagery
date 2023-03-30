from os.path import join
import argparse
from random import randint, sample
from glob import glob
from PIL import Image
from psychopy import core, prefs, visual, sound
from psychopy.hardware import keyboard
from psychopy.hardware.emulator import launchScan
import librosa


def run_miniblock(img_stimuli, audio_stimuli, window, n_stimuli=4, stim_len=4.0, cond='open'):
    '''Run a miniblock of the experiment.
            img_stimuli (dict): Contains the loaded images indexed by the stimulus name.
            audio_stimuli (dict): Contains the filenames of the .wav audio files indexed by the stimulus name.
            window (psychopy.visual.Window): Experiment display to present the stimuli.
            n_stimuli (int, optional): Number of stimuli to present in the miniblock.
            stim_len (float, optional): Number of seconds to present each stimuli.
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
    stim_keys = list(img_stimuli.keys())
    block_stims = sample(stim_keys, n_stimuli)
    for stim in block_stims:
        # Prepare the image stimulus.
        img_stim = visual.ImageStim(window, image=img_stimuli[stim], size=(2.0, 2.0))
        img_stim.draw()
        # Prepare the audio stimulus.
        audio_vec = audio_stimuli[stim][0].reshape(-1,1)
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
    ap.add_argument('-s', '--stimulus_time', type=float, default=1.5, help='Length of time to display each stimulus.')
    ap.add_argument('-d', '--delay_time', type=float, default=8.0, help='Length of time for fixation delay period between miniblocks.')
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
    #face_img_paths = sorted(glob('Stimuli/Images/People/*'))
    #face_audio_paths = sorted(glob('Stimuli/Audio/People/*.wav'))
    #letter_img_paths = sorted(glob('Stimuli/Images/Letters/*'))
    #letter_audio_paths = sorted(glob('Stimuli/Audio/Letters/*.wav'))
    #face_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in face_img_paths}
    #letter_imgs = {path.split('/')[-1].split('.jpg')[0].replace('_', ' '): Image.open(path) for path in letter_img_paths}
    #face_audio = {path.split('/')[-1].split('.wav')[0].replace('_', ' '): librosa.load(path, sr=48000) for path in face_audio_paths}
    #letter_audio = {path.split('/')[-1].split('.wav')[0].replace('_', ' '): librosa.load(path, sr=48000) for path in letter_audio_paths}

    #### SCANNER SYNCING: May need to get rid of launch scan?? ####
    MR_settings = {'TR': 1.5, 'sync': 'equal', 'volumes': 10.0, 'skip': 0.0}
    launchScan(win, MR_settings, mode='test', wait_msg='Waiting for pulse.')
    key_resp = keyboard.Keyboard()
    while True:
        allKeys = key_resp.getKeys(keyList=['equal'], waitRelease=False)
        if MR_settings['sync'] in allKeys:
            break

    # Run the experiment.
    n_blocks = 1
    for _ in range(n_blocks):
        win = run_miniblock(face_imgs, face_audio, win, n_stimuli=4, stim_len=args.stimulus_time, cond='open')
        win = run_miniblock(face_imgs, face_audio, win, n_stimuli=4, stim_len=args.stimulus_time, cond='closed')
        win = run_miniblock(letter_imgs, letter_audio, win, n_stimuli=4, stim_len=args.stimulus_time, cond='open')
        win = run_miniblock(letter_imgs, letter_audio, win, n_stimuli=4, stim_len=args.stimulus_time, cond='closed')
        
        # Add a fixation period
        message = visual.TextStim(win, text='+')
        message.draw()
        win.flip()
        core.wait(args.delay_time)

    # Clean things up.
    win.close()
    core.quit()
