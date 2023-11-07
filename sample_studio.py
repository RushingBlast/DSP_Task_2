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
                self.data = None
        self.time = None

        self.gui.dial_SNR.setMinimum(0)
        self.gui.dial_SNR.setMaximum(50)
        self.gui.dial_SNR.setValue(50)

# Connections
        # self.gui.dial_SNR.valueChanged.connect(self.sliderMoved)
        self.gui.dial_SNR.valueChanged.connect(self.Add_Noise)
        
        self.gui.btn_open_signal.clicked.connect(self.Open_CSV_File)

        # self.gui.btn_add_component.clicked.connect(self.add_sig_to_resultantGraph)

        # self.gui.listWidget.currentItemChanged.connect(self.plot_sigComponent)
        # self.gui.btn_remove_component.clicked.connect(self.delete_sigComponent_from_resultantGraph)
        # self.gui.btn_compose.clicked.connect(self.plot_resultant_sig_on_mainGraph)
        # self.gui.tabWidget.currentChanged.connect(self.set_focus_on_tab_change)
        
        # # Composer Fields
        # self.gui.lineEdit_amplitude.textEdited.connect(self.plot_sig_on_plot_widget_component)
        # self.gui.lineEdit_frequency.textEdited.connect(self.plot_sig_on_plot_widget_component)
        # self.gui.lineEdit_phase.textEdited.connect(self.plot_sig_on_plot_widget_component)
        
        # # Slider:
        # self.gui.horizontalSlider_sample_freq.valueChanged.connect(lambda: self.Renew_Intr(self.gui.horizontalSlider_sample_freq.value()))

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
        self.data = y_axis
        self.time = time
        self.plotOnMain(time[0:1000], y_axis[0:1000], Signal_Name)

    def Plot_Signal(self):
        pass

    def Add_Noise(self):
        self.gui.plot_widget_main_signal.clear()    
        
        # Define a function to calculate the power of a list of values
        def power(my_list):
            return [x**2 for x in my_list]

        # Calculate the power of the original signal
        powerr = power(self.data)
        
        # Get the Signal-to-Noise Ratio (SNR) in decibels from the GUI dial
        snr_db = self.gui.dial_SNR.value()
        
        # Calculate the average power of the signal
        signal_average_power = np.mean(powerr)
        
        # Convert the average signal power to decibels
        signal_average_power_db = 10 * np.log10(signal_average_power)
        
        # Calculate the noise power in decibels
        noise_db = signal_average_power_db - snr_db
        
        # Convert the noise power from decibels to watts
        noise_watts = 10 ** (noise_db / 10)
        
        # Generate random noise samples with a mean of 0 and standard deviation based on noise power
        noise = np.random.normal(0, np.sqrt(noise_watts), len(self.data))
        
        # Add the generated noise to the original signal
        noise_signal = self.data + noise
        
        # Plot the noisy signal on the main signal plot_widget in red
        self.gui.plot_widget_main_signal.plot(self.time, noise_signal, pen="r")
        
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
        self.gui.plot_widget_main_signal.clear()        
        self.gui.plot_widget_main_signal.plot(Time, Amplitude, pen="r")


import sys


def window():
    app = QApplication(sys.argv)
    win = Signal_Composer()

    win.show()
    sys.exit(app.exec_())


# main code
if __name__ == "__main__":
    window()
