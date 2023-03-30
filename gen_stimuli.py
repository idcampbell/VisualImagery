import argparse
from glob import glob
import numpy as np
import pandas as pd

def parse_args():
    '''Parse user arguments for how to generate the stimuli.
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--nBlocks', type=int, required=True, help='Number of blocks to randomly generate.')
    ap.add_argument('-s', '--subjID', type=str, required=True, help='Subject ID for which we are generating a run.')
    ap.add_argument('-r', '--runID', type=str, default='1', help='Run ID of the current run we\'re generating.')
    args = ap.parse_args()
    return args

if __name__=='__main__':
    # Set a random seed.
    seed = 8888
    np.random.seed(seed)
    # get user input for generating trial.
    args = parse_args()
    subj_id = args.subjID
    n_blocks = args.nBlocks
    run_id = args.runID
    print(subj_id)
    # Store the generated information to save later.
    col_names = ['subject', 'block', 'miniblock', 'stimulus', 'eye_cond', 'stim_category', 'stimulus_path']
    df = pd.DataFrame(np.zeros([n_blocks*8*4*4, 7]), columns=col_names)
    # Grab the filenames for the stimuli.
    face_img_paths = np.array(sorted(glob('Stimuli/Images/People/*.jpg')))
    letters_img_paths = np.array(sorted(glob('Stimuli/Images/Letters/*.jpg')))
    face_audio_paths = np.array(sorted(glob('Stimuli/Audio/People/*.wav')))
    letters_audio_paths = np.array(sorted(glob('Stimuli/Audio/Letters/*.wav')))
    # Explicitely define the miniblock structure.
    cat_cond = ['F', 'L', 'F', 'L', 'L', 'F', 'L', 'F']
    eye_pair = [('O', 'C'), ('O', 'C'), ('C', 'O'), ('C', 'O'), ('O', 'C'), ('O', 'C'), ('C', 'O'), ('C', 'O')]
    # Loop over blocks.
    i = 0
    for ib in range(n_blocks):
        inds = np.random.choice(16, 16, replace=False)
        inds1, inds2 = inds[:8], inds[8:]
        # Loop over miniblocks.
        for im in range(4):
            mini = miniblocks[i]
            for tini in mini:
                df, i = populate_df(df, eye_cond, pair, stimuli)
                


def populate_df(df, eye_cond, pair, stimuli, i):

