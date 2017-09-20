#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

# Módulo necessário

from epics import caput
import time

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
