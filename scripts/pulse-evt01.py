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


def configure_timing_modules_init():
    print('configuring timing modules (init)')
    write_pv(P+'AS-Glob:TI-EVG:ContinuousEvt-Sel', 0)
    write_pv(P+'AS-Glob:TI-EVG:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:ACDiv-SP', 30)
    write_pv(P+'AS-Glob:TI-EVG:ACEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVG:RFDiv-SP', 4)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    write_pv(P+'AS-Glob:TI-EVR-1:DevEnbl-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08State-Sel', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Width-SP', 7000)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Evt-SP', 1)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Polarity-Sel', 0)
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', 1)

def configure_timing_modules_cycle():
    configure_timing_modules_init()
    print('configuring timing modules (cycle)')
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', 1)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')

def configure_timing_modules_ramp():
    configure_timing_modules_init()
    print('configuring timing modules (ramp)')
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', WFMDATA_LENGTH)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'Continuous')
    write_pv(P+'AS-Glob:TI-EVG:ContinuousEvt-Sel', 1)

def configure_timing_modules_mig():
    configure_timing_modules_init()
    print('configuring timing modules (mig)')
    write_pv(P+'AS-Glob:TI-EVR-1:OTP08Pulses-SP', WFMDATA_LENGTH)
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
    write_pv(P+'AS-Glob:TI-EVG:Evt01ExtTrig-Cmd', 1)

def configure_timing_modules_stop():
    print('configuring timing modules (stop)')
    write_pv(P+'AS-Glob:TI-EVG:Evt01Mode-Sel', 'Disable')
    write_pv(P+'AS-Glob:TI-EVG:ContinuousEvt-Sel', 0)

def check_readback_pvs():
    pvs = [
        P+'AS-Glob:TI-EVG:DevEnbl-Sts',
        P+'AS-Glob:TI-EVG:ACDiv-RB',
        P+'AS-Glob:TI-EVG:ACEnbl-Sts',
        P+'AS-Glob:TI-EVG:ContinuousEvt-Sts',
        P+'AS-Glob:TI-EVG:RFDiv-RB',
        P+'AS-Glob:TI-EVG:Evt01Mode-Sts',
        P+'AS-Glob:TI-EVG:RFStatus-Mon',
        P+'AS-Glob:TI-EVR-1:DevEnbl-Sts',
        P+'AS-Glob:TI-EVR-1:OTP08State-Sts',
        P+'AS-Glob:TI-EVR-1:OTP08Width-RB',
        P+'AS-Glob:TI-EVR-1:OTP08Pulses-RB',
        P+'AS-Glob:TI-EVR-1:OTP08Evt-RB',
        P+'AS-Glob:TI-EVR-1:OTP08Polarity-Sts',
        P+'AS-Glob:TI-EVR-1:OTP08Pulses-RB',
        ]
    for pv in pvs:
        print("{0:40s}{1}".format(pv, epics.caget(pv)))


if __name__ == '__main__':
    parser = _argparse.ArgumentParser(description="Script for tests.")
    parser.add_argument(
        "mode", type=str,
        choices=('s', 'r', 'm', 'c', 'd', 'i'),
        help=
            "s to stop ramp; r to ramp; m to mig; c to cycle;" +
            " d to read PVs; i init config timing")
    args = parser.parse_args()

    if args.mode.lower().startswith('d'):
        check_readback_pvs()
    elif args.mode.lower().startswith('s'):
        configure_timing_modules_stop()
    elif args.mode.lower().startswith('i'):
        configure_timing_modules_init()
    elif args.mode.lower().startswith('c'):
        configure_timing_modules_cycle()
        print('triggering timing in cycle mode...')
        write_pv(P+'AS-Glob:TI-EVG:Evt01ExtTrig-Cmd', 1)
    elif args.mode.lower().startswith('r'):
        configure_timing_modules_ramp()
        print('triggering timing in ramp mode (signal generator)...')
    elif args.mode.lower().startswith('m'):
        configure_timing_modules_mig()
        print('triggering timing in mig mode (signal generator)...')
