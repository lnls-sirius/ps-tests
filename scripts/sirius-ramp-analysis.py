#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

"""Analysis script."""


from ps_ramp_tests import analysis


data = analysis.read_data(print_flag=True)
analysis.plot_data(data)
data = analysis.add_sync_upborder(data)
ramp_set = analysis.get_split_ramps_indices(data)
analysis.plot_ramps(data, ramp_set, sig_idx=0)
