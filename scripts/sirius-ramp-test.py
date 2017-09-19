#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

import time
import sys
from epics import caput, caget
import matplotlib.pyplot as plt
from siriuspy.magnet.util import generate_normalized_ramp

max_current = 10.0  # [A]
ref_current_3gev = max_current/1.05  # [A]
ramp = ref_current_3gev * generate_normalized_ramp()
curve1 = ramp

pvs = {'ti_stop':      'AS-Inj:TI-EVG1:STOPSEQ',
       'ti_run':       'AS-Inj:TI-EVG1:RUNSEQ',
       'ps_sync':      'SerialNetwork1:Sync',
       'ps1_opmode':   'BO-01U:PS-CH:OpMode-Sel',
       'ps2_opmode':   'BO-03U:PS-CH:OpMode-Sel',
       'ps1_wfmdata':  'BO-01U:PS-CH:WfmData-SP',
       'ps2_wfmdata':  'BO-03U:PS-CH:WfmData-SP',
       'ps1_pwrstate': 'BO-01U:PS-CH:PwrState-Sel',
       'ps2_pwrstate': 'BO-03U:PS-CH:PwrState-Sel',
       }

def sync_disable():
    """Disable synchronism."""
    caput(pvs['ti_stop'], 1)
    time.sleep(2.0)
    caput(pvs['ps_sync'], "Off")


def sync_enable():
    """Enable synchronism."""
    caput(pvs['ps_sync'], "On")
    time.sleep(2.0)
    caput(pvs['ti_run'], 1)


def opmode_set(opmode):
    """Set power supply mode."""
    caput(pvs['ps1_opmode'], opmode)
    caput(pvs['ps2_opmode'], opmode)


def wfmdata_send():
    """Send WfmData to power supplies."""
    sync_disable()
    opmode_set('SlowRef')
    caput(pvs['ps1_wfmdata'], ramp)
    caput(pvs['ps2_wfmdata'], ramp)
    time.sleep(2)


def pwrstate_set(state):
    """Set power supply PwrState mode."""
    caput(pvs['ps1_pwrstate'], state)
    caput(pvs['ps2_pwrstate'], state)


def pvs_print():
    """Print PV names and values."""
    for pv in pvs.values():
        value = caget(pv)
        print(pv, value)


def ramp_plot():
    """Plot reference ramp curve."""
    plt.plot(ramp, 'o')
    plt.show()


def test_start():
    """Start data acquisition."""
    pwrstate_set('On')
    sync_disable()
    wfmdata_send()
    opmode_set('RmpWfm')
    sync_enable()
    time.sleep(0.6)


def test_stop():
    """Stop data acquisition."""
    sync_disable()
    opmode_set('SlowRef')



def cmd_start():
    # Desliga o sistema de sincronismo

    caput("AS-Inj:TI-EVG1:STOPSEQ", 1)

    # Intervalo de 2 s

    time.sleep(2)

    # Desabilita o sincronismo via interface serial

    caput("SerialNetwork1:Sync", "Off")

    # Coloca a fonte BO-01U:PS-CH no modo SlowRef

    caput("BO-01U:PS-CH:OpMode-Sel", "SlowRef")

    # Envia a curva para a fonte BO-01U:PS-CH

    caput("BO-01U:PS-CH:WfmData-SP", curve1)

    # Coloca a fonte BO-01U:PS-CH no modo RmpWfm

    caput("BO-01U:PS-CH:OpMode-Sel", "RmpWfm")

    # Coloca a fonte BO-03U:PS-CH no modo SlowRef

    caput("BO-03U:PS-CH:OpMode-Sel", "SlowRef")

    # Envia a curva para a fonte BO-03U:PS-CH

    caput("BO-03U:PS-CH:WfmData-SP", curve1)

    # Coloca a fonte BO-03U:PS-CH no modo RmpWfm

    caput("BO-03U:PS-CH:OpMode-Sel", "RmpWfm")

    # Intervalo de 2 s

    time.sleep(2)

    # Habilita o sincronismo via interface serial

    caput("SerialNetwork1:Sync", "On")

    # Intervalo de 0,5 s

    time.sleep(0.5)

    # Liga o sistema de sincronismo

    caput("AS-Inj:TI-EVG1:RUNSEQ", 1)


def cmd_stop():
    # Desliga o sistema de sincronismo

    caput("AS-Inj:TI-EVG1:STOPSEQ", 1)

    # Intervalo de 2 s

    time.sleep(2)

    # Desabilita o sincronismo via interface serial

    caput("SerialNetwork1:Sync", "Off")

    # Coloca a fonte BO-01U:PS-CH no modo SlowRef

    caput("BO-01U:PS-CH:OpMode-Sel", "SlowRef")

    # Coloca a fonte BO-03U:PS-CH no modo SlowRef

    caput("BO-03U:PS-CH:OpMode-Sel", "SlowRef")


if __name__ == '__main__':
    actions = {'start': cmd_start,
               'stop': cmd_stop,
               'plot': ramp_plot,
               'pvs': pvs_print}
    if len(sys.argv) != 2 or sys.argv[1] not in actions.keys():
        print('Invalid syntax! Please specify action.')
        print('Valid actions:', list(actions.keys()))
    else:
        actions[sys.argv[1]]()
