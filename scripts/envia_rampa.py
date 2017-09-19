#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

# Módulos necessários

from epics import caput
import math
import time

# Geração de curva triangular de 2000 pontos com amplitude máxima, sendo 1000 pontos de subida e
# outros 1000 pontos de descida.

curve1 = []
for i in range(1000):
    curve1.append((10.0 * i) / 999)
for i in range(1000):
    curve1.append(10.0 - curve1[i])

curve2 = []
for i in range(2000):
    curve2.append(10 * math.sin((2 * math.pi * i) / 1999))

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
