from cProfile import label
import sys
from matplotlib.pyplot import xlabel
from gui import Ui_MainWindow
import os
import numpy as np
import math
from scipy.fftpack import fft, fftfreq
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
import numpy as np
from scipy.fftpack import fft, fftfreq
import pyqtgraph as pg


#TODO - Make auto naming in composer more robust (not urgent AT ALL)

    



class SignalGUI(Ui_MainWindow):
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        
        
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
        for point in range(len(sig_to_add.y_axis_values)):
            self.resultant_sig[1][point] += sig_to_add.y_axis_values[point]
        
    
    def subtract_sig_from_result(self, sig_to_subtract):
        for point in range(len(sig_to_subtract.y_axis_values)):
            self.resultant_sig[1][point] -= sig_to_subtract.y_axis_values[point]


class Signal_Composer(QtWidgets.QMainWindow):
    exported_signal_index = "resultant_signal_from_composer"
    def __init__(self):
        super(Signal_Composer, self).__init__()
        self.gui = SignalGUI()
        self.gui.setupUi(self)
        self.gui.tabWidget.setCurrentIndex(0)
        self.data = None
        self.time = None
        
        self.index_for_nameless = 0 # An index to append to default signal component name in composer
        self.index_for_duplicate = 0 # An index to append to components with similar names
        
        self.composed_result = class_sinusoidal() # Holds an initial dummy signal with no values
        
        self.component_dict = {} # Dictionary to hold the components of the composed signal
        
        self.gui.dial_SNR.setMinimum(0)
        self.gui.dial_SNR.setMaximum(50)
        self.gui.dial_SNR.setValue(50)
        self.gui.lbl_snr_level.setText(f"SNR Level: (50dB)")
        

        ######################################################### SHORTCUTS #########################################################
        openShortcut = QShortcut(QKeySequence("ctrl+o"), self)
        openShortcut.activated.connect(self.Open_CSV_File)
        
        switchTabsShortcut = QShortcut(QKeySequence("Ctrl + Tab"), self)
        switchTabsShortcut.activated.connect(self.Switch_Tabs)
        
        
        
        
        
        ###################################################### UI CONNECTIONS #######################################################
        
        self.gui.dial_SNR.valueChanged.connect(self.Add_Noise)
        
        self.gui.btn_open_signal.clicked.connect(self.Open_CSV_File)

        self.gui.btn_add_component.clicked.connect(self.Add_Sig_Component)

        self.gui.list_sig_components.currentItemChanged.connect(self.Plot_Sig_Component_From_ListWidget)
        self.gui.btn_remove_component.clicked.connect(self.Remove_Sig_Component)
        self.gui.btn_compose.clicked.connect(self.Save_Composed_Signal)
        self.gui.tabWidget.currentChanged.connect(self.Set_Focus_On_Tab_Change)
        
        # Composer Fields
        self.gui.field_amplitude.textEdited.connect(self.Plot_Field_Contents)
        self.gui.field_frequency.textEdited.connect(self.Plot_Field_Contents)
        self.gui.field_phase.textEdited.connect(self.Plot_Field_Contents)
        
        # # Slider:
        # self.gui.horizontalSlider_sample_freq.valueChanged.connect(lambda: self.Renew_Intr(self.gui.horizontalSlider_sample_freq.value()))


    ######################################################### Definitions #########################################################
   
   
    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Misc Methods                                                          #
    #-----------------------------------------------------------------------------------------------------------------------------#

   
    
    def Set_Focus_On_Tab_Change(self):
        # Sets focus on the name field in composer or 'Open File' button in viewer 
        if self.gui.tabWidget.currentIndex() == 1:
            self.gui.field_name.setFocus()
        else:
            self.gui.btn_open_signal.setFocus()
            
    def Switch_Tabs(self):
        self.gui.tabWidget.setCurrentIndex(int(not bool(self.gui.tabWidget.currentIndex)))
    # def Switch_Tabs(self):
    #     if self.gui.tabWidget.currentIndex == 0:
    #         self.gui.tabWidget.setCurrentIndex(1)
    #     elif self.gui.tabWidget.currentIndex == 1:
    #         self.gui.tabWidget.setCurrentIndex(0)
            
            
    
    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Viewer Methods                                                        #
    #-----------------------------------------------------------------------------------------------------------------------------#
    
    
    def Slider_Changed(self):
        pass
    

        

    def Open_CSV_File(self):
        # try:
        # Create file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        # Path of selected file
        path, _ = QFileDialog.getOpenFileName( self, "Open Data File", "", "CSV Files (*.csv);;DAT Files (*.dat)", options=options)
        
        # Set signal name to file name
        Signal_Name = path.split('/')[-1].split(".")[0]
        
        #load the data from csv
        data = np.genfromtxt(path, delimiter=',')
        
        # take time values from first column
        time = list(data[1:, 0])
        # take y values from second column
        y_axis = list(data[1:, 1])
        
        self.data = y_axis[0:1000]
        self.time = time[0:1000]
        # Plot time and y values on main plot
        self.Plot_On_Main(time[0:1000], y_axis[0:1000])
        # except:
        #     return

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


    # Plots a given signal on the main plot (plot_widget_main_signal)
    def Plot_On_Main(self, Time, Amplitude):
        self.gui.plot_widget_main_signal.clear()        
        self.gui.plot_widget_main_signal.plot(Time, Amplitude, pen="r")
        sample_points = np.arange(0, 1, 1 / 1000)
        scatter = pg.ScatterPlotItem(pos=np.column_stack((sample_points, self.data)), size=2, pen='w')
        self.gui.plot_widget_main_signal.addItem(scatter)
        
    def Clear_Sig_Information(self):
        pass
    
    def Plot_Result_Signal(self):
        pass




    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Composer Methods                                                        #
    #-----------------------------------------------------------------------------------------------------------------------------#
    
    
    # Adds signal component to plot_widget_composed_signal
    def Add_Sig_Component(self):
        
        
        # Create signal from fields
        sig_comp = self.Create_Sig_From_Fields()
        
        # Add item to list_sig_component and append to component_dict
        self.gui.list_sig_components.addItem(sig_comp.name)
        self.component_dict[sig_comp.name] = sig_comp
        
        # Add new component to composed signal
        self.composed_result.add_sig_to_result(sig_comp)
        
        # Plot new composed signal
        self.gui.plot_widget_composed.clear()
        self.gui.plot_widget_composed.plot(self.composed_result.resultant_sig[0], self.composed_result.resultant_sig[1], pen = 'r')
        print(sig_comp.name)
        
        # Prepare for new component input
        self.gui.plot_widget_component.clear()
        self.Clear_Input_Fields()
        
        self.gui.field_name.setFocus()
        
    # Adds signal component to plot_widget_composed_signal
    def Remove_Sig_Component(self):
        
    
        self.gui.plot_widget_component.clear()
        
        # Remove item from component_dict
        comp_to_be_removed = self.component_dict.pop(self.gui.list_sig_components.currentItem().text())
        
        # Remove item from list_sig_component
        self.gui.list_sig_components.takeItem(self.gui.list_sig_components.currentRow())
        
        if len(self.component_dict) == 0:
            self.gui.plot_widget_composed.clear()
            return
        
        
        # Remove selected component from composed signal
        self.composed_result.subtract_sig_from_result(comp_to_be_removed)
        
        # Plot new composed signal
        self.gui.plot_widget_composed.clear()
        self.gui.plot_widget_composed.plot(self.composed_result.resultant_sig[0], self.composed_result.resultant_sig[1], pen = 'r')
        
        self.gui.field_name.setFocus()

        
    
    
    # Returns a class_sinusoidal object with the field inputs 
    def Create_Sig_From_Fields(self):
        
        name = self.gui.field_name.text()
        freq = self.Return_Zero_At_Empty_String(self.gui.field_frequency.text(), 1)
        amp = self.Return_Zero_At_Empty_String(self.gui.field_amplitude.text(), 1)
        phase = self.Return_Zero_At_Empty_String(self.gui.field_phase.text(), 0)
        
        if name == "":
            name = f"sig_{self.index_for_nameless}"
            self.index_for_nameless +=1
        
        elif name in self.component_dict.keys():
            name = f"{name}_{self.index_for_duplicate}"
            self.index_for_nameless +=1
            
            
                
        new_sig = class_sinusoidal(name, float(freq), float(amp), float(phase))
        return new_sig
        
    # Plots the selected signal component from list_sig_components on plot_widget_component
    def Plot_Sig_Component_From_ListWidget(self):
        self.gui.plot_widget_component.clear()
        
        sig_component = self.component_dict[self.gui.list_sig_components.currentItem().text()]
        self.gui.plot_widget_component.plot(sig_component.time_values, sig_component.y_axis_values, pen = "r")
    
    
    # Plot field contents on plot_widget_component
    def Plot_Field_Contents(self):
        self.gui.plot_widget_component.clear()
        temp_sig = self.Create_Sig_From_Fields()
        self.gui.plot_widget_component.plot(temp_sig.time_values, temp_sig.y_axis_values, pen = "r")
    
    # Clear Input Fields
    def Clear_Input_Fields(self):
        self.gui.field_name.clear()
        self.gui.field_amplitude.clear()
        self.gui.field_frequency.clear()
        self.gui.field_phase.clear()

    # Saves composed signal and opens it in the viewer
    def Save_Composed_Signal(self):
        
        self.Export_Composed_Signal_As_CSV()
        
        # Plot composed signal on plot_widget_main_signal
        self.Plot_On_Main(self.composed_result.resultant_sig[0], self.composed_result.resultant_sig[1] )
        

        # Reset everything for next composition
        self.gui.plot_widget_composed.clear()
        self.gui.list_sig_components.clear()    
        self.composed_result = class_sinusoidal()
        self.component_dict = {}
        
    # Exports the signal as a CSV file
    def Export_Composed_Signal_As_CSV(self,f_sample = 0, file_name="composed_signal_data"):
        # self.composed_result.resultant_sig.append([f_sample])
        df = pd.DataFrame(self.composed_result.resultant_sig).transpose()
        # df.columns = ['Time', 'Amplitude', 'F_Sampling']
        df.columns = ['Time', 'Amplitude', ]
        df.to_csv(file_name + '.csv', index=False)
        
    
    
    def Return_Zero_At_Empty_String(self, string, value):
        if string == "":
            return f"{value}"
        else:
            return string                           






def window():
    app = QApplication(sys.argv)
    win = Signal_Composer()

    win.show()
    sys.exit(app.exec_())


# main code
if __name__ == "__main__":
    window()
