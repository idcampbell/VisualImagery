import argparse
import os
import warnings
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
    # Stop deprecation warning bs they're annoying.
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    # Set a random seed.
    seed = 8888
    np.random.seed(seed)
    # get user input for generating trial.
    args = parse_args()
    subj_id = args.subjID
    n_blocks = args.nBlocks
    run_id = args.runID
    # Grab the filenames for the stimuli.
    face_img_paths = np.array(sorted(glob('Stimuli/Images/People/*.jpg')))
    letters_img_paths = np.array(sorted(glob('Stimuli/Images/Letters/*.jpg')))
    face_audio_paths = np.array(sorted(glob('Stimuli/Audio/People/*.wav')))
    letters_audio_paths = np.array(sorted(glob('Stimuli/Audio/Letters/*.wav')))
    audio_paths = np.stack([face_audio_paths, letters_audio_paths])
    img_paths = np.stack([face_img_paths, letters_img_paths])
    # Explicitely define the miniblock structure.
    category_conds = [('F', 'F', 'L', 'L'), ('F', 'F', 'L', 'L'), ('L', 'L', 'F', 'F'), ('L', 'L', 'F', 'F')]
    eye_conds = [('O', 'C', 'O', 'C'), ('C', 'O', 'C', 'O'), ('O', 'C', 'O', 'C'), ('C', 'O', 'C', 'O')]
    # Loop over blocks and store the generated information to save later.
    col_names = ['subject', 'block', 'miniblock', 'category', 'eye_cond', 'img_path', 'audio_path']
    results = []
    for ib in range(n_blocks):
        inds = np.random.choice(16, 16, replace=False).reshape(2,-1)
        # Loop over miniblocks.
        for im in range(4):
            mb_df = pd.DataFrame(np.zeros([8*4, 7]), columns=col_names)
            mb_df.loc[:,'subject'] = subj_id
            mb_df.loc[:, 'block'] = ib+1
            mb_df.loc[:, 'miniblock'] = im+1+ib*4
            mb_df.loc[:, 'category'] = np.repeat(category_conds[im], 8)
            mb_df.loc[:, 'eye_cond'] = np.repeat(eye_conds[im], 8)
            # Get the proper stimulus file paths.
            eye_cond_inds = (np.array(eye_conds[im])=='O').astype(int)
            stim_cond_inds = (np.array(category_conds[im])=='F').astype(int)
            mb_stim_inds = inds[eye_cond_inds,:].ravel()
            mb_df.loc[:, 'audio_path'] = audio_paths[stim_cond_inds,:][np.repeat([0,1,2,3], 8), mb_stim_inds]
            mb_df.loc[:, 'img_path'] = img_paths[stim_cond_inds,:][np.repeat([0,1,2,3], 8), mb_stim_inds]
            results.append(mb_df)
    # Save the dataframe.
    results_df = pd.concat(results).reset_index(drop=True)
    os.makedirs('Stimuli/CSVs', exist_ok=True)
    results_df.to_csv(os.path.join('Stimuli/CSVs', f'{subj_id}_run{run_id}.csv'))
