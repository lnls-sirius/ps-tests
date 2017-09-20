#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

"""Analysis script."""

import os as _os
import sys as _sys
# import numpy as _np
# import matplotlib.pyplot as _plt
from pathlib import Path as _Path

from ps_ramp_tests import analysis


def plot_raw_data(fname):
    """Plot raw power supply acquisition data."""
    data = analysis.read_data(fname=fname, print_flag=True)
    analysis.plot_data(data)
    return data


def compare_with_ref_ramp(fname=None, signal_idx=0):
    """Compare digitilized signals with reference ramp."""
    data = plot_raw_data(fname=fname)
    data = analysis.add_sync_upborder(data)
    ramp_set = analysis.get_split_ramps_indices(data)
    analysis.plot_ramps(data, ramp_set, sig_idx=0)


if __name__ == '__main__':
    fname = _os.path.join(str(_Path.home()),
                          'troca', 'teste2_17-09-12_1544.txt')
    if len(_sys.argv) != 2:
        print('Invalid arguments!')
    elif _sys.argv[1] == 'plot-raw-data':
        plot_raw_data()
    elif _sys.argv[1] == 'compare-with-ref-ramp':
        compare_with_ref_ramp(fname=fname, signal_idx=0)
