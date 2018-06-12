# DINDIN Meryll
# June 04, 2018
# Dreem Headband Sleep Phases Classification Challenge

import argparse, warnings

from package.models import *

# Main algorithm

if __name__ == '__main__':

    # Initialize the arguments
    prs = argparse.ArgumentParser()
    # Mandatory arguments
    prs.add_argument('-m', '--marker', help='Giving identity to the model', type=str, default=None)
    prs.add_argument('-b', '--batch', help='Batch size for training instance', type=int, default=64)
    prs.add_argument('-d', '--decrease', help='Number of epochs to decrease the dropout', type=int, default=50)
    prs.add_argument('-n', '--tail', help='Number of merge layers', type=int, default=10)
    # Channels acceleration
    prs.add_argument('--acc_cv2', help='Acceleration | Method CONV2D', type=str, default='F')
    prs.add_argument('--acc_cv1', help='Acceleration | Method CONV1D', type=str, default='F')
    prs.add_argument('--acc_ls1', help='Acceleration | Method LSTM1D', type=str, default='F')
    prs.add_argument('--acc_cvl', help='Acceleration | Method CVLSTM', type=str, default='F')
    # Channels norm acceleration
    prs.add_argument('--n_a_cv1', help='Norm Acceleration | Method CONV1D', type=str, default='F')
    prs.add_argument('--n_a_ls1', help='Norm Acceleration | Method LSTM1D', type=str, default='F')
    prs.add_argument('--n_a_cvl', help='Norm Acceleration | Method CVLSTM', type=str, default='F')
    prs.add_argument('--n_a_dlc', help='Norm Acceleration | Method DUALCV', type=str, default='F')
    # Channels electroencephalograms
    prs.add_argument('--eeg_cv2', help='Electroencephalograms | Method CONV2D', type=str, default='F')
    prs.add_argument('--eeg_cv1', help='Electroencephalograms | Method CONV1D', type=str, default='F')
    prs.add_argument('--eeg_ls1', help='Electroencephalograms | Method LSTM1D', type=str, default='F')
    prs.add_argument('--eeg_dlc', help='Electroencephalograms | Method DUALCV', type=str, default='F')
    prs.add_argument('--eeg_atd', help='Electroencephalograms | Method ENCODE', type=str, default='F')
    prs.add_argument('--eeg_atc', help='Electroencephalograms | Method ENCODE', type=str, default='F')
    prs.add_argument('--eeg_cvl', help='Electroencephalograms | Method CVLSTM', type=str, default='F')
    prs.add_argument('--eeg_tda', help='Electroencephalograms | Method TDACV1', type=str, default='F')
    # Channels norm electroencephalograms
    prs.add_argument('--n_e_cv1', help='Norm EEG | Method CONV1D', type=str, default='F')
    prs.add_argument('--n_e_ls1', help='Norm EEG | Method LSTM1D', type=str, default='F')
    prs.add_argument('--n_e_cvl', help='Norm EEG | Method CVLSTM', type=str, default='F')
    prs.add_argument('--n_e_dlc', help='Norm EEG | Method DUALCV', type=str, default='F')
    # Channels wavelets transforms
    prs.add_argument('--wav_cv2', help='Wavelet Transforms | Method CONV2D', type=str, default='F')
    prs.add_argument('--wav_cv1', help='Wavelet Transforms | Method CONV1D', type=str, default='F')
    prs.add_argument('--wav_ls1', help='Wavelet Transforms | Method LSTM1D', type=str, default='F')
    prs.add_argument('--wav_dlc', help='Wavelet Transforms | Method DUALCV', type=str, default='F')
    prs.add_argument('--wav_cvl', help='Wavelet Transforms | Method CVLSTM', type=str, default='F')
    # Channels oxygen measurements
    prs.add_argument('--oxy_cv1', help='Oxymeter | Method CONV1D', type=str, default='F')
    prs.add_argument('--oxy_ls1', help='Oxymeter | Method LSTM1D', type=str, default='F')
    prs.add_argument('--oxy_dlc', help='Oxymeter | Method DUALCV', type=str, default='F')
    prs.add_argument('--oxy_cvl', help='Oxymeter | Method CVLSTM', type=str, default='F')
    # Basic channels
    prs.add_argument('--feature', help='Features | Method DENSE', type=str, default='T')
    prs.add_argument('--dis_fft', help='FFT | Method DENSE', type=str, default='T')
    prs.add_argument('--dis_pca', help='PCA | Method DENSE', type=str, default='T')
    # Parse the arguments
    prs = prs.parse_args()

    # Define the corresponding channels
    dic = {
           'with_acc_cv2': prs.acc_cv2 == 'T',
           'with_acc_cv1': prs.acc_cv1 == 'T',
           'with_acc_ls1': prs.acc_ls1 == 'T',
           'with_acc_cvl': prs.acc_cvl == 'T',
           'with_n_a_cv1': prs.n_a_cv1 == 'T',
           'with_n_a_ls1': prs.n_a_ls1 == 'T',
           'with_n_a_cvl': prs.n_a_cvl == 'T',
           'with_n_a_dlc': prs.n_a_dlc == 'T',
           'with_eeg_cv2': prs.eeg_cv2 == 'T',
           'with_eeg_cv1': prs.eeg_cv1 == 'T',
           'with_eeg_ls1': prs.eeg_ls1 == 'T',
           'with_eeg_dlc': prs.eeg_dlc == 'T',
           'with_eeg_atd': prs.eeg_atd == 'T',
           'with_eeg_atc': prs.eeg_atc == 'T',
           'with_eeg_cvl': prs.eeg_cvl == 'T',
           'with_eeg_tda': prs.eeg_tda == 'T',
           'with_n_e_cv1': prs.n_e_cv1 == 'T',
           'with_n_e_ls1': prs.n_e_ls1 == 'T',
           'with_n_e_cvl': prs.n_e_cvl == 'T',
           'with_n_e_dlc': prs.n_e_dlc == 'T',
           'with_wav_cv2': prs.wav_cv2 == 'T',
           'with_wav_cv1': prs.wav_cv1 == 'T',
           'with_wav_ls1': prs.wav_ls1 == 'T',
           'with_wav_dlc': prs.wav_dlc == 'T',
           'with_wav_cvl': prs.wav_cvl == 'T',
           'with_oxy_cv1': prs.oxy_cv1 == 'T',
           'with_oxy_ls1': prs.oxy_ls1 == 'T',
           'with_oxy_dlc': prs.oxy_dlc == 'T',
           'with_oxy_cvl': prs.oxy_cvl == 'T',
           'with_fea': prs.feature == 'T',
           'with_fft': prs.dis_fft == 'T',
           'with_pca': prs.dis_pca == 'T'
           }

    # Launch the model
    mod = DL_Model('./dataset/DTB_Headband.h5', dic, marker=prs.marker)
    mod.learn(patience=10, dropout=0.5, decrease=prs.decrease, batch=prs.batch, n_tail=prs.tail)