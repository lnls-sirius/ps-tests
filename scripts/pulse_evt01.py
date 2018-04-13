#!/usr/bin/env python-sirius

import time
import epics


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
    run()
