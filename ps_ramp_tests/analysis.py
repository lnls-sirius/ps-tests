#!/usr/bin/env python-sirius

"""Script for Ramp data analysis."""

import os as _os
import numpy as _np
import matplotlib.pyplot as _plt
from pathlib import Path as _Path
from siriuspy.magnet.util import generate_normalized_ramp


_fname = _os.path.join(str(_Path.home()), 'troca', 'teste2_17-09-12_1544.txt')
_sample_rate = 50*1000  # [Hz]
_sync_sig_idx = None
_sync_sig_level = 5.0
_max_current = 10.0  # [A]
_ref_current_3gev = _max_current/1.05  # [A]
_ref_ramp = _ref_current_3gev * generate_normalized_ramp()


# curve1 = []
# for i in range(1000):
#     curve1.append((10.0/1.05 * i) / 999)
# for i in range(1000):
#     curve1.append(10.0/1.05 - curve1[i])
# _ref_ramp = curve1

def read_data(fname=None, print_flag=True):
    """Read data from file."""
    global _sync_sig_idx
    if fname is None:
        fname = _fname
    data = _np.loadtxt(fname, dtype=float, delimiter='\t')
    get_sync_signal_index(data)
    if print_flag:
        print('sample rate   [kHz]  : {}'.format(_sample_rate/1000))
        print('number of points     : {}'.format(data.shape[0]))
        print('time interval [s]    : {}'.format(data.shape[0]/_sample_rate))
        print('number of signals    : {}'.format(data.shape[1]))
        print('index of sync signal : {}'.format(_sync_sig_idx))
    return data


def add_sync_upborder(data, sync_sig_level=_sync_sig_level):
    """Find trigger borders in data."""
    new_data = _np.hstack((data,
                           _np.zeros((data.shape[0], 1), dtype=data.dtype)))
    sync = data[:, _sync_sig_idx]
    for i in range(1, len(sync)):
        if sync[i-1] < sync_sig_level/2.0 < sync[i]:
            new_data[i, -1] = 1.0
    return new_data


def get_sync_signal_index(data=None):
    """Get index of sync signal column."""
    global _sync_sig_idx
    if data is not None and _sync_sig_idx is None:
        idx = None
        for i in range(data.shape[1]):
            d = data[:, i]
            if _np.all(d > -2.0) and _np.all(d < 7.0) and _np.any(d > 2.0):
                idx = i
        _sync_sig_idx = idx
    return _sync_sig_idx


def plot_data(data, max_idx=None):
    """Plot data."""
    if max_idx is None:
        max_idx = data.shape[0]
    nr_sigs = data.shape[1]
    fig, axes = _plt.subplots(nrows=nr_sigs, ncols=1)
    axes[0].plot(data[:max_idx, 0])
    axes[1].plot(data[:max_idx, 1])
    axes[2].plot(data[:max_idx, 2])
    axes[3].plot(data[:max_idx, 3])
    if nr_sigs == 5:
        axes[4].plot(data[:max_idx, 4])
    _plt.show()


def get_split_ramps_indices(data):
    """Return array of ramp indices (where sync is triggered)."""
    sync_trig = data[:, -1]
    idx, *_ = _np.where(sync_trig != 0)
    threshold = max(_np.diff(idx))/2.0
    # finds indices of all ramp starts
    last_trigger = 0
    ramp_starts = []
    for i in range(len(sync_trig)):
        if sync_trig[i] == 1:
            if i - last_trigger > threshold:
                ramp_starts.append(i)
            last_trigger = i
    # return ramp_starts
    ramps = []
    for i in range(len(ramp_starts)-1):
        ramp = []
        j = ramp_starts[i]
        while len(ramp) < len(_ref_ramp):
            if sync_trig[j] == 1:
                ramp.append(j)
            j += 1
        ramps.append(ramp)
    return ramps


def plot_ramps(data, ramp_set, sig_idx):
    """Plot ramps for a specified signal and reference."""
    for ramp in ramp_set:
        _plt.plot(data[min(ramp):max(ramp)+1, sig_idx], 'k.')
    d = [i - ramp_set[0][0] for i in ramp_set[0]]
    _plt.plot(d, _ref_ramp, 'r.')
    _plt.show()
