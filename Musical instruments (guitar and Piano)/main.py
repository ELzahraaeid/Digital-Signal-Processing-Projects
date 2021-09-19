import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from gui import Ui_MainWindow
import sounddevice as sd
import math


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.piano_freq=[110,123.74,130.81,146.83,164.81,147.61,196,220,293.66,329.63]
        self.buttongroup=QtWidgets.QButtonGroup()
        self.radiolist=[self.ui.b1,self.ui.b2,self.ui.b3,self.ui.b4,self.ui.b5,self.ui.b6,self.ui.b7,self.ui.b8,self.ui.b9,self.ui.b10,self.ui.b11,self.ui.b12,self.ui.b13]
        for i in range (len(self.radiolist)):
            self.buttongroup.addButton(self.radiolist[i],i)

        self.which_fret=[]


        self.fs = 8000


        self.list_freq=[[82.41,87.31,92.50,98,103.83,110,116.54,123.47,130.81,138.59,146.83,155.56,164.81],
                        [110,116.54,123.47,130.81,138.59,146.83,155.56,164.81,174.61,185,196,207.65,220],
                        [146.83,155.56,164.81,174.61,185,196,207.65,220,233.08,246.94,261.63,277.18,293.66],
                        [196,207.65,220,233.08,246.94,261.63,277.18,293.66,311.13,329.63,349.23,369.99,392],
                        [246.94,261.63,277.18,293.66,311.13,329.63,349.23,369.99,392,415.3,440,466.16,493.88],
                        [329.63,349.23,369.99,392,415.3,440,466.16,493.88,523.25,554.37,587.33,622.25,659.26]]

        self.ui.btn1.clicked.connect(lambda:self.karplus_strong(5))
        self.ui.btn2.clicked.connect(lambda: self.karplus_strong(4))
        self.ui.btn3.clicked.connect(lambda: self.karplus_strong(3))
        self.ui.btn4.clicked.connect(lambda: self.karplus_strong(2))
        self.ui.btn5.clicked.connect(lambda: self.karplus_strong(1))
        self.ui.btn6.clicked.connect(lambda: self.karplus_strong(0))

        self.ui.bt1.clicked.connect(lambda: self.piano(0))
        self.ui.bt2.clicked.connect(lambda: self.piano(1))
        self.ui.bt3.clicked.connect(lambda: self.piano(2))
        self.ui.bt4.clicked.connect(lambda: self.piano(3))
        self.ui.bt5.clicked.connect(lambda: self.piano(4))
        self.ui.bt6.clicked.connect(lambda: self.piano(5))
        self.ui.bt7.clicked.connect(lambda: self.piano(6))
        self.ui.bt8.clicked.connect(lambda: self.piano(7))
        self.ui.bt9.clicked.connect(lambda: self.piano(8))
        self.ui.bt10.clicked.connect(lambda: self.piano(9))

    def karplus_strong(self,i):

        self.which_fret = [self.buttongroup.checkedId()]
        print(self.which_fret)
        n_samples = 2 * self.fs
        freq=self.list_freq[i][self.which_fret[0]]

        if int(freq) in range (50,150):
            stretch_factor=1
        elif int(freq) in range (150,250):
            stretch_factor = 2.1
        elif int(freq) in range (250,350):
            stretch_factor = 3.5
        elif int(freq) in range (350,450):
            stretch_factor = 4
        else:
            stretch_factor = 8
        wavetable_size = self.fs // int(freq)
        wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)

        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            r = np.random.binomial(1, 1 - 1 / stretch_factor)
            if r == 0:
                wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size

        sd.play(samples,self.fs)
        sd.wait()




    def piano(self,i):
        freq =self.piano_freq[i]
        print(freq)
        sampleRate = 44100

        t = np.linspace(0, 20, sampleRate * 5)

        y = np.sin(2 * np.pi * freq * t) * np.exp(-0.0004 * 2 * np.pi * freq * t)

        sd.play(y, 2 * sampleRate)
        sd.wait()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
