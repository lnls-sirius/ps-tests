#!/usr/bin/env python-sirius

from PyQt5.QtWidgets import *
import ps_ramp_tests.analysis as a
import numpy as _np
import matplotlib.pyplot as _plt

# fname = '../data/test8_17-11-13_1005.txt'
# a.make_analysis(fname)
#
# fname = '../data/test9_17-11-13_1006.txt'
# a.make_analysis(fname)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cw = QWidget()
        self.setCentralWidget(self.cw)

        self.layout = QVBoxLayout()
        self.cw.setLayout(self.layout)


        self.btn = QPushButton("Click to Select Data File")
        self.layout.addWidget(self.btn)
        self.rbgbox = QGroupBox('Select Nr. Signals:')
        self.rbgbox2 = QGroupBox('Select Nr. Points in Ramp:')
        self.layout.addWidget(self.rbgbox)
        self.layout.addWidget(self.rbgbox2)
        self.btn.clicked.connect(self.getfile)

        self.rblayout = QHBoxLayout()
        self.rbgbox.setLayout(self.rblayout)
        self.rbtn1 = QRadioButton("1")
        self.rbtn2 = QRadioButton("2")
        self.rbtn3 = QRadioButton("3")
        self.rbtn3.setChecked(True)
        self.rblayout.addWidget(self.rbtn1)
        self.rblayout.addWidget(self.rbtn2)
        self.rblayout.addWidget(self.rbtn3)

        self.rblayout2 = QHBoxLayout()
        self.rbgbox2.setLayout(self.rblayout2)
        self.rbtn2000 = QRadioButton("2000")
        self.rbtn4000 = QRadioButton("4000")
        self.rbtn4000.setChecked(True)
        self.rblayout2.addWidget(self.rbtn2000)
        self.rblayout2.addWidget(self.rbtn4000)


    def getfile(self):
        if self.rbtn1.isChecked():
            nr_signals = 1
        elif self.rbtn2.isChecked():
            nr_signals = 2
        elif self.rbtn3.isChecked():
            nr_signals = 3
        if self.rbtn2000.isChecked():
            nrpts = 2000
        elif self.rbtn4000.isChecked():
            nrpts = 4000
        result = QFileDialog.getOpenFileName(None,
                                             'Open file',
                                             '/home/fac_files/lnls-sirius/ps-tests/data',
                                             "data files (*.txt)")
        fname = result[0]
        if fname:
            a.make_analysis(fname, nr_signals, nrpts)



app = QApplication([])
window = MyApp()
window.show()
app.exec_()
