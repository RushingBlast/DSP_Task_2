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


#TODO - implement the component dict into sig_comp creation
#TODO - Tweak things in such a way that makes Plot_Sig_Component only plot a signal, no creation
#TODO - Add Sig_comp plotting dynamically as user is filling the fields
#TODO - restore functionality to btn_add_component
#TODO - did I mention implementing the component dict into the functions?
#TODO - restore fucntionality to the list widget
#TODO - restore functionality to btn_remove_component
    



class SignalGUI(Ui_MainWindow):
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.tabWidget.setCurrentIndex(0)
        
        
class class_sinusoidal():
    
    # Initialize the sinusoidal with a list of 1000 time values and 1000 zeroes
    resultant_sig = [np.linspace(0, 2, 1000, endpoint=False), [0] * 1000]
    
    def __init__(self, name="", frequency = 1.0, amplitude = 1.0, phase = 0.0):
        
        self.name = name
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        
        self.time_values = np.linspace(0, 2, 1000, endpoint= False)
        
        # Creates a sin function with Sin(2 * pi * F * T + phase) and multiply it with the amplitude
        self.y_axis_values = amplitude * np.sin(2 * math.pi * frequency * self.time_values + phase)
    
    def add_sig_to_result(self, sig_to_add):
        for point in sig_to_add:
            self.resultant_sig[1][point] += sig_to_add[1][point]
        
    
    def subtract_sig_from_result(self, sig_to_subtract):
        for point in sig_to_subtract:
            self.resultant_sig[1][point] -= sig_to_subtract[1][point]


class Signal_Composer(QtWidgets.QMainWindow):
    exported_signal_index = "resultant_signal_from_composer"
    def __init__(self):
        super(Signal_Composer, self).__init__()
        self.gui = SignalGUI()
        self.gui.setupUi(self)
        self.data = None
        self.time = None
        
        self.composer_comps = {} # Dict to hold the components of the composed signal
        
        self.gui.dial_SNR.setMinimum(0)
        self.gui.dial_SNR.setMaximum(50)
        self.gui.dial_SNR.setValue(50)
        self.gui.lbl_snr_level.setText(f"SNR Level: (50dB)")
        
        
# Connections
        # self.gui.dial_SNR.valueChanged.connect(self.sliderMoved)
        self.gui.dial_SNR.valueChanged.connect(self.Add_Noise)
        
        self.gui.btn_open_signal.clicked.connect(self.Open_CSV_File)

        self.gui.btn_add_component.clicked.connect(self.Plot_Sig_Component)

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

    def Slider_Changed(self):
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
        
        # Get the Signal-to-Noise Ratio (SNR) in decibels from the GUI dial
        snr_db = self.gui.dial_SNR.value()
        
        # Set label text to SNR dB value
        self.gui.lbl_snr_level.setText(f"SNR Level: ({snr_db}dB)")
        
        # Define a function to calculate the power of a list of values
        def power(my_list):
            return [x**2 for x in my_list]

        # Calculate the power of the original signal
        power_orig_signal = power(self.data)
        
        
        # Calculate the average power of the signal
        signal_average_power = np.mean(power_orig_signal)
        
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

    
    # Returns a class_sinusoidal object with the field inputs 
    def Create_Sig_From_Fields(self):
        
        name = self.Return_Zero_At_Empty_String(self.gui.field_name.text())
        freq = self.Return_Zero_At_Empty_String(self.gui.field_frequency.text())
        amp = self.Return_Zero_At_Empty_String(self.gui.field_amplitude.text())
        phase = self.Return_Zero_At_Empty_String(self.gui.field_phase.text())
                
        new_sig = class_sinusoidal(name, float(freq), float(amp), float(phase))
        return new_sig
        
    # Plots a signal ocmponent on plot_widget_component
    def Plot_Sig_Component(self):
        self.gui.plot_widget_component.clear()
        
        sig_component = self.Create_Sig_From_Fields()
        
        self.gui.plot_widget_component.plot(sig_component.resultant_sig, pen = "r", name = sig_component.name)
        
        pass

    def Delete_Signal_From_Result(self):
        pass


    def Save_Result(self):
        pass


    @classmethod
    def export_resultant_as_csv(cls, file_name="signal_data"):
        pass
    
    
    def Return_Zero_At_Empty_String(string):
        if string == "":
            return "0"
        else:
            return string                           
 
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
