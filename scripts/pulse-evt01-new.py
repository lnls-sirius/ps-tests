#!/usr/bin/env python-sirius

import time
import epics
import argparse as _argparse

P = 'T'
TIMEOUT = 0.1
SLEEP = False
WAIT = True
WFMDATA_LENGTH = 4000

def write_pv(pvname, value):
    epics.caput(pvname, value, wait=WAIT)
    if SLEEP:
        time.sleep(TIMEOUT)


def configure_timing_modules_basic():
    print('configuring timing modules (basic)')
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:ACDiv-SP', 30)
    write_pv(P+'AS-Glob:TI-EVG:ACEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:ContinuousEvt-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:RFDiv-SP', 4)
    write_pv(P+'AS-Glob:TI-EVR-1:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08State-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Width-SP', 7000)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Evt-SP', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Polarity-Sel', 0)

def configure_timing_modules_cycle():
    print('configuring timing modules (cycle)')
    write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', 1)

def configure_timing_modules_ramp():
    print('configuring timing modules (ramp)')
    write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'Continuous')
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', WFMDATA_LENGTH)

def configure_timing_modules_stop():
    print('configuring timing modules (stop)')
    write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 0)

# def configure_timing_modules(cycle=True):
#     print('Configuring Timing Modules to ' + ('cycle' if cycle else 'ramp'))
#     write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External' if cycle else 'Continuous')
#     write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
#     write_pv(P+'AS-Glob:TI-EVG:ACDiv-SP', 30)
#     write_pv(P+'AS-Glob:TI-EVG:ACEnbl-Sel', 1)
#     write_pv(P+'AS-Glob:TI-EVG:ContinuousEvt-Sel', 1)
#     write_pv(P+'AS-Glob:TI-EVG:RFDiv-SP', 4)
#     write_pv(P+'AS-Glob:TI-EVR-1:DevEnbl-Sel', 1)
#     write_pv(P+'AS-Glob:TI-EVR-1:OTP08State-Sel', 1)
#     write_pv(P+'AS-Glob:TI-EVR-1:OTP08Width-SP', 7000)
#     write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', 1 if cycle else 4000)
#     write_pv(P+'AS-Glob:TI-EVR-1:OTP08Evt-SP', 1)
#     write_pv(P+'AS-Glob:TI-EVR-1:OTP08Polarity-Sel', 0)


# def run(n):
#     pv = epics.PV(P+'AS-Glob:TI-EVG:Evt01ExtTrig-Cmd')
#     try:
#         while True:
#             t0 = time.time()
#             pv.put(1, wait=WAIT)
#             time.sleep(0.500)
#             print('time interval {:.4f} ms'.format((time.time()-t0)*1000))
#             n -= 1
#             if n == 0:
#                 break
#     except KeyboardInterrupt:
#         pass


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
    parser.add_argument(
        '-s', "--stop", action='store_true', default=False,
        help="If you want to stop timing pulses this must be present.")
    args = parser.parse_args()

    if args.configure.lower().startswith('y'):
        configure_timing_modules_basic()
    if args.cycle:
        configure_timing_modules_cycle()
        print('triggering timing in cycle mode...')
        pv = epics.PV(P+'AS-Glob:TI-EVG:Evt01ExtTrig-Cmd')
        pv.put(1, wait=WAIT)
    if args.ramp:
        configure_timing_modules_ramp()
        print('triggering timing in ramp mode (signal generator)...')
    if args.stop:
        configure_timing_modules_stop()
