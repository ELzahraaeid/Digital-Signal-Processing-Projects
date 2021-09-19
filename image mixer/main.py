from imageModel import ImageModel
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QSlider,QMessageBox
from gui import Ui_MainWindow
import cv2 as cv
from modesEnum import Modes
import logging


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        logging.basicConfig(filename='logFile.log',level=logging.INFO,format='%(levelname)s:%(message)s')

        self.ui.clearb.clicked.connect(self.clear_img)

        self.img_size = [0, 0]
        self.imgshow = [self.ui.img1, self.ui.img2, self.ui.plt_img1, self.ui.plt_img2, self.ui.out_img1, self.ui.out_img2]
        self.buttons = [self.ui.but_1, self.ui.but_2]
        self.options_draw = ["Magnitude_Spectral", "Phase_Spectral", "Real_Spectral", "Imaginary_Spectral"]
        self.comb_input = [self.ui.comb_img1, self.ui.comb_img2]
        self.comb_indx = [0, 0]
        self.getpath = ['', '']
        self.disable_enable=[self.ui.comb_out1,self.ui.comb_out2,self.ui.comb_options1,self.ui.comb_options2,self.ui.comb_out,self.ui.but_2,self.ui.comb_img2]
        self.slider = [self.ui.slider1, self.ui.slider2]
        self.slider_val = [0, 0]
        self.slider_label = [self.ui.label_1, self.ui.label_2]

        # mixing lists&&signal
        self.component_index = [0, 0]

        self.y = [self.ui.comb_options1, self.ui.comb_options2]
        self.x1 = [['mag', 'phase', 'real', 'imagin', 'unit mag', 'unit phase'],
                   ['phase', 'mag', 'real', 'imagin', 'unit mag', 'unit phase']]

        self.comb_choose_out_option = ['mag', 'phase']
        self.output_picture = [0, 0]


        for i in range(len(self.imgshow)):
            self.imgshow[i].ui.histogram.hide()
            self.imgshow[i].ui.roiBtn.hide()
            self.imgshow[i].ui.menuBtn.hide()
            self.imgshow[i].ui.roiPlot.hide()

        # setting options of draw image in combobox
        for i in range(len(self.options_draw)):
            self.ui.comb_img1.addItem(self.options_draw[i])
            self.ui.comb_img2.addItem(self.options_draw[i])

        self.comb_input[0].activated.connect(lambda: self.add_spectral(0))
        self.comb_input[1].currentIndexChanged.connect(lambda: self.add_spectral(1))

        #slider setting
        for i in range(2):
            self.slider[i].setTickInterval(10)
            self.slider[i].setMinimum(0)
            self.slider[i].setMaximum(100)

        self.slider[0].valueChanged.connect(lambda: self.slider_val_change(0))
        self.slider[1].valueChanged.connect(lambda: self.slider_val_change(1))

        for i in range (2):
            self.connect_but(i)

        for i in range (2):
            self.y[i].addItems(self.x1[i])

        self.ui.comb_options1.currentIndexChanged.connect(self.change_comb)
        self.ui.comb_options2.currentTextChanged.connect(self.get_text_comb2)

        self.ui.comb_out1.currentIndexChanged.connect(lambda: self.combindx(0))
        self.ui.comb_out2.currentIndexChanged.connect(lambda: self.combindx(1))
        self.ui.comb_out.currentIndexChanged.connect(lambda: self.show_img(0))

        self.disable()


    def connect_but(self, but_n):
        self.buttons[but_n].clicked.connect(lambda: self.add_file(but_n))
        if but_n==0:
            logging.info('add image 1 button pressed')
        else:
            logging.info('add image 2 button pressed')

    def add_file(self,butt_num):
        filename = QFileDialog(self).getOpenFileName()

        path = filename[0]

        if path != '':

            img = cv.imread(path, 0)
            x = img.shape


            if butt_num==0:

                z=1


            else:
                z=0


            if self.img_size[z] == 0 or x == self.img_size[z]:

                self.img_size[butt_num]=x
                self.getpath[butt_num] = path

                self.imgshow[butt_num].show()

                self.imgshow[butt_num].setImage(img.T)

                self.enable()
                self.ui.comb_options2.setEnabled(False)
                self.add_spectral(butt_num)
                self.add_out()

            else:
                self.error_msg()




    def error_msg(self):
        msg = QMessageBox()
        msg.setWindowTitle("matching size faild")
        msg.setText("not the same size!")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()
        logging.info('try to add image not the same size')


    def add_spectral(self,i):
        self.comb_indx[i]=self.comb_input[i].currentIndex()
        if i==0:
             logging.info('add spectral of image 1')
        else:
            logging.info('add spectral of image 2')
        if self.getpath[i] !='':
           x=ImageModel(self.getpath[i])

           if self.comb_indx[i] == 0:
                draw = 20 * np.log(x.magnitude)

           if self.comb_indx[i] == 1:
                draw = (x.phase)

           if self.comb_indx[i] == 2:
               draw = (x.real)

           if self.comb_indx[i] == 3:
              draw = (x.imaginary)

           self.imgshow[i + 2].setImage(draw.T)

    def clear_img(self):
        for i in range(len(self.imgshow)):
            self.imgshow[i].clear()
            self.img_size = [0, 0]
            self.getpath = ['', '']
            self.slider_val=[0,0]
            self.disable()
        logging.info('clear button pressed ')

    def disable(self):
        for i in range (len(self.disable_enable)):
            self.disable_enable[i].setEnabled(False)

    def enable(self):
        for i in range(len(self.disable_enable)):
             self.disable_enable[i].setEnabled(True)


    def combindx(self,i):
        if i==0:
            self.component_index[i]=self.ui.comb_out1.currentIndex()
            logging.info('change the component you want to mix in component1')
        else:
            self.component_index[i] = self.ui.comb_out2.currentIndex()
            logging.info('change the component you want to mix in component2')
        self.add_out()

    def show_img(self,i):
        self.output_picture[i]=self.ui.comb_out.currentIndex()
        logging.info('change the widget of output')
        self.add_out()

    def change_comb(self):
        self.ui.comb_options2.setEnabled(True)
        current = self.ui.comb_options1.currentText()
        self.enable_options()
        if current == "mag":
            self.hide_options_comb2([1,2,3,4])

        elif current == "phase":
            self.hide_options_comb2([0, 2, 3, 5])

        elif current == "real":
            self.hide_options_comb2([0,1, 2, 4, 5])

        elif current == "imagin":
            self.hide_options_comb2([0,1,3,4,5])


        elif current == "unit phase":
            self.hide_options_comb2([0, 2, 3, 5])
        else:
            self.hide_options_comb2([1, 2, 3, 4])


    def slider_val_change(self, i):
        self.slider_val[i] = self.slider[i].value()
        self.slider_label[i].setText(str(self.slider_val[i]))
        if i==0:
            logging.info('changing the value of slider 1')
        else:
            logging.info('changing the value of slider 2')
        self.add_out()

    def enable_options(self):
        for i in range (6):
            self.ui.comb_options2.view().setRowHidden(i, False)

    def hide_options_comb2(self,i):
        for l in range (len(i)):
            self.ui.comb_options2.view().setRowHidden(i[l], True)

    def get_text_comb2(self):
        self.comb_choose_out_option[1] = self.y[1].currentText()
        self.comb_choose_out_option[0] = self.y[0].currentText()
        logging.info('change the combobox of what spectral you want to mix')
        self.add_out()


    def add_out(self):

        if self.getpath[self.component_index[0]] != '':
              mix_comp1=ImageModel(self.getpath[self.component_index[0]])
        if self.getpath[self.component_index[1]] != '':
              mix_comp2 = ImageModel(self.getpath[self.component_index[1]])

        if self.comb_choose_out_option[0] == 'mag' and self.comb_choose_out_option[1] == 'phase':
           out= mix_comp1.mix(mix_comp2,float((self.slider_val[0])/100) ,float((self.slider_val[1])/100) ,Modes.magnitudeAndPhase)



        elif self.comb_choose_out_option[0] == 'phase' and self.comb_choose_out_option[1] == 'mag':
           out= mix_comp2.mix(mix_comp1,float((self.slider_val[1])/100) ,float((self.slider_val[0])/100) ,Modes.magnitudeAndPhase)



        elif self.comb_choose_out_option[0] == 'real' and self.comb_choose_out_option[1] == 'imagin':
            out = mix_comp1.mix(mix_comp2, float((self.slider_val[0]) / 100), float((self.slider_val[1]) / 100),
                                Modes.realAndImaginary)




        elif self.comb_choose_out_option[0] == 'imagin' and self.comb_choose_out_option[1] == 'real':
            out = mix_comp2.mix(mix_comp1, float((self.slider_val[1]) / 100), float((self.slider_val[0]) / 100),
                                Modes.realAndImaginary)


        elif self.comb_choose_out_option[0] == 'mag' and self.comb_choose_out_option[1] == 'unit phase':
            out = mix_comp1.mix(mix_comp2, float((self.slider_val[0]) / 100), float((self.slider_val[1]) / 100),
                                Modes.magnitudeAndunitPhase)



        elif self.comb_choose_out_option[0] == 'unit phase' and self.comb_choose_out_option[1] == 'mag':

            out = mix_comp2.mix(mix_comp1, float((self.slider_val[1]) / 100), float((self.slider_val[0]) / 100),
                                Modes.magnitudeAndunitPhase)

        elif self.comb_choose_out_option[0] == 'unit mag' and self.comb_choose_out_option[1] == 'phase':
            out = mix_comp1.mix(mix_comp2, float((self.slider_val[0]) / 100), float((self.slider_val[1]) / 100),
                                Modes.unitmagnitudeAndPhase)



        elif self.comb_choose_out_option[0] == 'phase' and self.comb_choose_out_option[1] == 'unit mag':
            out = mix_comp2.mix(mix_comp1, float((self.slider_val[0]) / 100), float((self.slider_val[1]) / 100),
                                Modes.unitmagnitudeAndPhase)

        else:
            out = mix_comp1.mix(mix_comp2, float((self.slider_val[0]) / 100), float((self.slider_val[1]) / 100),
                                Modes.unitmagnitudeAndunitPhase)
        if self.output_picture[0] == 0:

            self.ui.out_img1.setImage(out.T)

        else:
            self.ui.out_img2.setImage(out.T)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()


