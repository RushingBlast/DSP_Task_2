from cProfile import label

from matplotlib.pyplot import xlabel
from gui import Ui_MainWindow
import os
import numpy as np
import math
from scipy.fftpack import fft, fftfreq
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import numpy as np
from scipy.fftpack import fft, fftfreq
import pyqtgraph as pg

class SignalGUI(Ui_MainWindow):
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.tabWidget.setCurrentIndex(0)


class Signal_Composer(QtWidgets.QMainWindow):
    exported_signal_index = "resultant_signal_from_composer"
    def __init__(self):
        super(Signal_Composer, self).__init__()
        self.gui = SignalGUI()
        self.gui.setupUi(self)
        

# Connections
        self.gui.dial_SNR.valueChanged.connect(self.sliderMoved)
        self.gui.dial_SNR.valueChanged.connect(self.noise_addition)
        
        self.gui.btn_open_signal.clicked.connect(self.open_sig_file)

        self.gui.btn_add_component.clicked.connect(self.add_sig_to_resultantGraph)

        self.gui.listWidget.currentItemChanged.connect(self.plot_sigComponent)
        self.gui.btn_remove_component.clicked.connect(self.delete_sigComponent_from_resultantGraph)
        self.gui.btn_compose.clicked.connect(self.plot_resultant_sig_on_mainGraph)
        self.gui.tabWidget.currentChanged.connect(self.set_focus_on_tab_change)
        
        # Composer Fields
        self.gui.lineEdit_amplitude.textEdited.connect(self.plot_sig_on_plot_widget_component)
        self.gui.lineEdit_frequency.textEdited.connect(self.plot_sig_on_plot_widget_component)
        self.gui.lineEdit_phase.textEdited.connect(self.plot_sig_on_plot_widget_component)
        
        # Slider:
        self.gui.horizontalSlider_sample_freq.valueChanged.connect(lambda: self.Renew_Intr(self.gui.horizontalSlider_sample_freq.value()))

    def Slide_Changed(self):
        pass
    

    def Tab_Focus_Change(self):
        pass

    def Open_CSV_File(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        path, _ = QFileDialog.getOpenFileName( self, "Open Data File", "", "CSV Files (*.csv);;DAT Files (*.dat)", options=options)
        Signal_Name = path.split('/')[-1].split(".")[0]
        data = np.genfromtxt(path, delimiter=',')
        time = list(data[1:, 0])
        y_axis = list(data[1:, 1])
        self.plotOnMain(time[0:1000], y_axis[0:1000], Signal_Name)
        self.data = y_axis
        self.time = time
        pass

    def Plot_Signal(self):
        pass

    def Add_Noise(self):
        pass
        
    def Clear_Sig_Information(self):
        pass
    
    def Plot_Result_Signal(self):
        pass


 
    def Plot_Sig_Component(self):
        pass

    def Delete_Signal_From_Result(self):
        pass


    def Save_Result(self):
        pass


    @classmethod
    def export_resultant_as_csv(cls, file_name="signal_data"):
        pass

        
    @classmethod
    def return_zero_at_emptyString(cls, string):
        pass                           
 
    def Renew_Intr(self, Freq):
        pass

    def plotOnMain(self, Time, Amplitude, Name):
        pass


import sys


def window():
    app = QApplication(sys.argv)
    win = Signal_Composer()

    win.show()
    sys.exit(app.exec_())


# main code
if __name__ == "__main__":
    window()
