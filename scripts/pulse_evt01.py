#!/usr/bin/env python-sirius

import time
import epics
import argparse as _argparse

P = 'TEST-'

def configure_timing_modules(cycle=True):
    print('Configuring Timing Modules to ' + ('cycle' if cycle else 'ramp'))
    epics.caput(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    epics.caput(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    epics.caput(P+'AS-Glob:TI-EVG:RFDiv-SP', 4)
    epics.caput(P+'AS-Glob:TI-EVR-1:DevEnbl-Sel', 1)
    epics.caput(P+'AS-Glob:TI-EVR-1:OTP00Width-SP', 7000)
    epics.caput(P+'AS-Glob:TI-EVR-1:OTP00State-Sel', 1)
    epics.caput(P+'AS-Glob:TI-EVR-1:OTP00Evt-SP', 1)
    epics.caput(P+'AS-Glob:TI-EVR-1:OTP00Pulses-SP', 1 if cycle else 4000)


def run(n):
    pv = epics.PV(P+'AS-Glob:TI-EVG:Evt01ExtTrig-Cmd')
    try:
        while True:
            t0 = time.time()
            pv.value = 1
            time.sleep(0.500)
            print('time interval {:.4f} ms'.format((time.time()-t0)*1000))
            n -= 1
            if n == 0:
                break
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = _argparse.ArgumentParser(description="Script for tests.")
    parser.add_argument(
        "configure", type=str, default='yes',
        help="'yes' if you want to configure timing modules. Else 'no'")
    parser.add_argument(
        '-c', "--cycle", action='store_true', default=False,
        help="If you want to perform cycle this must be present.")
    parser.add_argument(
        '-r', "--ramp", action='store_true', default=False,
        help="If you want to perform ramp this must be present.")
    args = parser.parse_args()

    if args.configure.lower().startswith('y'):
        configure_timing_modules(args.cycle)
    if args.cycle:
        run(1)
    if args.ramp:
        run(0)
