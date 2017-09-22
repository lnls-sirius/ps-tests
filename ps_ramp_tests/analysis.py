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


def get_pwrsupply_names():
    """Return PS names."""
    return ('BO-01U-PS-CH',
            'BO-01U-PS-CV',
            'BO-03U-PS-CH',
            'BO-03U-PS-CV',
            )


def get_reference_ramp():
    """Return reference ramp."""
    return _ref_ramp


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


def plot_ramp_repeatibility(data, ramp_set):
    """Plot ramps repeatibility and comparw with reference."""
    ref = [i - ramp_set[0][0] for i in ramp_set[0]]
    f, (ax0, ax1, ax2) = _plt.subplots(3, sharex=True, sharey=True)
    psnames = get_pwrsupply_names()
    axes = [ax0, ax1, ax2]
    for sig_idx in range(3):
        for ramp in ramp_set:
            datum = data[min(ramp):max(ramp)+1, sig_idx]
            axes[sig_idx].plot(datum, 'k.')
        axes[sig_idx].plot(ref, _ref_ramp, 'r.')
        axes[sig_idx].grid(True)
        axes[sig_idx].set_ylabel('{} Current [A]'.format(psnames[sig_idx]))
    ax0.set_title(('Ramp repeatibility ({} black) and comparison '
                   'with reference (1 red)').format(len(ramp_set)))
    _plt.xlabel('Sample Index')
    _plt.show()
    return ref, _ref_ramp


def plot_ramp_dispersion(data, ramp_set):
    """Plot ramps repeatibility and comparw with reference."""
    ppm = _max_current/1e6
    max_size = None
    for ramp in ramp_set:
        x = list(range(min(ramp), max(ramp)+1))
        max_size = len(x) if max_size is None else min(max_size, len(x))
    avg = _np.zeros((max_size, 3))
    std_ppm = _np.zeros((max_size, 3))
    max_ppm = _np.zeros((max_size, 3))
    min_ppm = _np.zeros((max_size, 3))
    for sig_idx in range(3):
        stat = _np.zeros((len(ramp_set), max_size))
        for i, ramp in enumerate(ramp_set):
            x = list(range(min(ramp_set[0]), max(ramp_set[0])+1))
            y = data[min(ramp):max(ramp)+1, sig_idx]
            stat[i, :] = y[:max_size]
        avg[:, sig_idx] = _np.mean(stat, axis=0)
        std_ppm[:, sig_idx] = _np.std(stat, axis=0) / ppm
        max_ppm[:, sig_idx] = (_np.max(stat, axis=0) -
                               _np.mean(stat, axis=0)) / ppm
        min_ppm[:, sig_idx] = (_np.min(stat, axis=0) -
                               _np.mean(stat, axis=0)) / ppm
    # plot data
    f, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = \
        _plt.subplots(3, 2, sharex=True, sharey=True)
    psnames = get_pwrsupply_names()
    ax0.plot(std_ppm[:, 0], 'b.')
    ax2.plot(std_ppm[:, 1], 'b.')
    ax4.plot(std_ppm[:, 2], 'b.')
    ax1.plot(max_ppm[:, 0], 'b.')
    ax1.plot(min_ppm[:, 0], 'b.')
    ax3.plot(max_ppm[:, 1], 'b.')
    ax3.plot(min_ppm[:, 1], 'b.')
    ax5.plot(max_ppm[:, 2], 'b.')
    ax5.plot(min_ppm[:, 2], 'b.')
    ax0.grid(True)
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    ax5.grid(True)
    ax0.set_ylabel('{} [ppm]'.format(psnames[0]))
    ax2.set_ylabel('{} [ppm]'.format(psnames[1]))
    ax4.set_ylabel('{} [ppm]'.format(psnames[2]))
    ax1.set_ylabel('{} [ppm]'.format(psnames[0]))
    ax3.set_ylabel('{} [ppm]'.format(psnames[1]))
    ax5.set_ylabel('{} [ppm]'.format(psnames[2]))
    ax0.set_title('Disp. (std) - {} ramps'.format(len(ramp_set)))
    ax1.set_title('Disp. (MinMax) - {} ramps'.format(len(ramp_set)))
    ax4.set_xlabel('Sample Index')
    ax5.set_xlabel('Sample Index')
    _plt.show()

    return max_size, avg, std_ppm, max_ppm, min_ppm

def plot_linear_tracking(data, ramp_set, max_size, avg):
    """Plot linear tracking."""

    d = avg[:, 0]
    min_idx = _np.where(d >= 10/1.05/20.0)[0][0]
    max_idx = _np.where(d >= 10/1.05)[0][0]
    lims = list(range(min_idx, max_idx))
    x = _np.array(list(range(min(ramp_set[0]), max(ramp_set[0])+1)))
    x = x[lims]
    ppm = _max_current/1e6

    f, axes = _plt.subplots(3, 2, sharex=True, sharey=False)
    ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = axes
    psnames = get_pwrsupply_names()

    for sig_idx in range(3):
        y = avg[lims, sig_idx]
        pfit = _np.polyfit(x, y, 1)
        yfit = _np.polyval(pfit, x)
        for i, ramp in enumerate(ramp_set):
            y = data[min(ramp):max(ramp)+1, sig_idx]
            y = y[lims]
            diff_ppm = (y-yfit)/ppm
            axes[sig_idx][1].plot(x, diff_ppm, 'k.')
            axes[sig_idx][0].plot(x, y, 'k.')
        axes[sig_idx][0].set_ylabel('{}'.format(psnames[sig_idx]))
        #axes[sig_idx][1].set_ylabel('{}'.format(psnames[sig_idx]))
        axes[sig_idx][0].plot(x, yfit, 'r')
        axes[sig_idx][0].grid(True)
        axes[sig_idx][1].grid(True)
    axes[-1][0].set_xlabel('Sample Index')
    axes[-1][1].set_xlabel('Sample Index')
    axes[0][0].set_title('Ramp current [A]')
    axes[0][1].set_title('Tracking error [ppm]')
    _plt.show()

def plot_linear_tracking_amongst_ps(data, ramp_set, max_size, avg):
    """Plot linear tracking."""

    d = avg[:, 0]
    min_idx = _np.where(d >= 10/1.05/20.0)[0][0]
    max_idx = _np.where(d >= 10/1.05)[0][0]
    lims = list(range(min_idx, max_idx))
    x = _np.array(list(range(min(ramp_set[0]), max(ramp_set[0])+1)))
    x = x[lims]
    ppm = _max_current/1e6

    y = (avg[lims, 0]+avg[lims, 1]+avg[lims, 2])/3.0
    pfit = _np.polyfit(x, y, 1)
    yfit = _np.polyval(pfit, x)
    for sig_idx in range(3):
        for i, ramp in enumerate(ramp_set):
            y = data[min(ramp):max(ramp)+1, sig_idx]
            y = y[lims]
            diff_ppm = (y-yfit)/ppm
            _plt.plot(x, diff_ppm, 'k.')
    _plt.title('Tracking error amongst PS [ppm]')
    _plt.xlabel('Sample Index')
    _plt.ylabel('Error [ppm]')
    _plt.grid(True)
    _plt.show()
