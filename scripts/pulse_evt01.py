#!/usr/bin/env python-sirius

import time
import epics
import argparse as _argparse


def configure_timing_modules(cycle=True):
    print('Configuring Timing Modules to ' + ('cycle' if cycle else 'ramp'))
    epics.caput('AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    epics.caput('AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    epics.caput('AS-Glob:TI-EVR-1DevEnbl-Sel', 1)
    epics.caput('AS-Glob:TI-EVR-1OTP00Width-SP', 7000)
    epics.caput('AS-Glob:TI-EVR-1OTP00State-Sel', 1)
    epics.caput('AS-Glob:TI-EVR-1OTP00Evt-SP', 1)
    epics.caput('AS-Glob:TI-EVR-1OTP00Pulses-SP', 1 if cycle else 4000)


def run():
    pv = epics.PV('AS-Glob:TI-EVG:Evt01ExtTrig-Cmd')
    try:
        while True:
            t0 = time.time()
            pv.value = 1
            time.sleep(0.500)
            print((time.time()-t0)*1000)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = _argparse.ArgumentParser(description="Script for tests.")
    parser.add_argument(
        "configure", type=str, default='yes',
        help="'yes' if you want to configure timing modules. Else 'no'")
    parser.add_argument(
        '-c', "--cycle", action='store_true', default=False,
        help="If you want to perform cycling this must be present.")
    args = parser.parse_args()

    if args.configure.lower().startswith('y'):
        configure_timing_modules(args.cycle)
    run()
