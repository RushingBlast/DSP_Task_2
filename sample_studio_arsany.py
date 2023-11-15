import sys
from gui import Ui_MainWindow
import numpy as np
import math
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
import numpy as np
import pyqtgraph as pg
import csv
from scipy.interpolate import interp1d


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


    def reset_resultant_sig(self):
        self.resultant_sig = [np.linspace(0, 2, 1000, endpoint=False), [0] * 1000]




class Signal_Composer(QtWidgets.QMainWindow):
    exported_signal_index = "resultant_signal_from_composer"
    def __init__(self):
        super(Signal_Composer, self).__init__()
        self.gui = SignalGUI()
        self.gui.setupUi(self)
        self.gui.tabWidget.setCurrentIndex(0)
        self.data = None
        self.time = None
        self.fs = None
        self.components_freq = []
        self.noisy_signal = None

        self.Time_Values = []
        self.Samples = []

        self.index_for_nameless = 0 # An index to append to default signal component name in composer
        self.index_for_duplicate = 0 # An index to append to components with similar names
        
        self.composed_result = class_sinusoidal() # Holds an initial dummy signal with no values
        
        self.component_dict = {} # Dictionary to hold the components of the composed signal

        self.gui.dial_SNR.setMinimum(0)
        self.gui.dial_SNR.setMaximum(50)
        self.gui.dial_SNR.setValue(50)
        self.gui.lbl_snr_level.setText(f"SNR Level: (50dB)")
        
        self.gui.horizontalSlider_sample_freq.setEnabled(False)
        


        ######################################################### SHORTCUTS #########################################################
        openShortcut = QShortcut(QKeySequence("ctrl+o"), self)
        openShortcut.activated.connect(self.Open_CSV_File)
        
        switchTabsShortcut = QShortcut(QKeySequence("Ctrl + Tab"), self)
        switchTabsShortcut.activated.connect(self.Switch_Tabs)
        
        
        
        
        
        ###################################################### UI CONNECTIONS #######################################################
        self.gui.horizontalSlider_sample_freq.valueChanged.connect(self.sampling_points_plot)  # Connect the valueChanged signal to a function
        self.gui.horizontalSlider_sample_freq.valueChanged.connect(self.print)  # Connect the valueChanged signal to a function

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
        
        

    ######################################################### Definitions #########################################################
   
   
    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Misc Methods                                                          #
    #-----------------------------------------------------------------------------------------------------------------------------#
# slider values
    def print(self):
        print(self.gui.horizontalSlider_sample_freq.value())
    
    def Set_Focus_On_Tab_Change(self):
        # Sets focus on the name field in composer or 'Open File' button in viewer 
        if self.gui.tabWidget.currentIndex() == 1:
            self.gui.field_name.setFocus()
        else:
            self.gui.btn_open_signal.setFocus()
            
    def Switch_Tabs(self):
        self.gui.tabWidget.setCurrentIndex(int(not bool(self.gui.tabWidget.currentIndex)))
            
            
    
    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Viewer Methods                                                        #
    #-----------------------------------------------------------------------------------------------------------------------------#
    
    
    def Slider_Changed(self):

        pass
    
    def components_freq_adding(self):
        
        self.components_freq.append(int(self.gui.field_frequency.text()))

    def get_max_freq(self):
    
        return max(self.components_freq)
        

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
        
        self.fs = int(data[1, 2])

        self.data = y_axis[0:1000]
        self.time = time[0:1000]
        # Plot time and y values on main plot
        self.Plot_On_Main(self.time, self.data)


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
        self.noisy_signal = self.data + noise
        
        # Plot the noisy signal on the main signal plot_widget in red
        self.Plot_On_Main(self.time, self.noisy_signal)

    # Plots a given signal on the main plot (plot_widget_main_signal)
    def Plot_On_Main(self, time, data):
        self.gui.plot_widget_main_signal.clear()        
        self.gui.plot_widget_main_signal.plot(time, data, pen="r")
        
        # freq_slider_enabled and limits
        self.gui.horizontalSlider_sample_freq.setEnabled(True)
        self.gui.horizontalSlider_sample_freq.setMinimum(1)
        self.gui.horizontalSlider_sample_freq.setMaximum(self.fs)
        self.gui.horizontalSlider_sample_freq.setValue(1)


        
    def sampling_points_plot(self):
        self.gui.plot_widget_main_signal.clear()

        fs = self.gui.horizontalSlider_sample_freq.value()

        if self.noisy_signal is None:
            self.Samples = []
            self.Time_Values = []
            for index in range(0, len(self.time), int(len(self.time)/fs)):
                self.Samples.append(self.data[index])
                self.Time_Values.append(self.time[index])

            # Plot the original signal
            self.gui.plot_widget_main_signal.plot(self.time, self.data, pen="r", name="Original Signal")
            # Plot the sampled points
            self.gui.plot_widget_main_signal.plot(self.Time_Values, self.Samples, pen=None, symbol='o', symbolSize=5, name="Sampled Points")
            
            # if self.Samples is not []:
            #     self.interploation()

        else:
            self.Samples = []
            self.Time_Values = []
            for index in range(0, len(self.time), int(len(self.time)/fs)):
                self.Samples.append(self.noisy_signal[index])
                self.Time_Values.append(self.time[index])
            # Plot the original signal
            self.gui.plot_widget_main_signal.plot(self.time, self.noisy_signal, pen="r", name="Original Signal")
            # Plot the sampled points
            self.gui.plot_widget_main_signal.plot(self.Time_Values, self.Samples, pen=None, symbol='o', symbolSize=5, name="Sampled Points")
            
            # if self.Samples is not []:
            #     self.interploation()

        # # Interpolate sampled points with linear interpolation
        # interp_func = interp1d(Time_Values, Samples, kind='linear')
        # interpolated_values = interp_func(self.time)

        # # Plot the interpolation
        # # self.gui.plot_widget_main_signal.plot(self.time, interpolated_values, pen="b", name="Interpolated Signal")

        # # Calculate the difference and plot it
        # difference = np.subtract(self.data, interpolated_values)

        # self.gui.plot_widget_difference.clear()
        # self.gui.plot_widget_difference.plot(self.time, difference, pen="g", name="Difference")

        # # Optionally, plot the restored signal without points
        # self.gui.plot_widget_restored_signal.clear()
        # self.gui.plot_widget_restored_signal.plot(self.time, interpolated_values, pen="y", name="Restored Signal")


    # def interploation(self):
    #     # # Generate 1000 points centered at 0.5 seconds
    #     # x = np.linspace(0, 10, 1000)
    #     # # Calculate sinc function values
    #     # y = x**2 

    #     # interploated = []
    #     # for i in range(0,len(self.Samples)):
    #     #     a = self.Samples[i] * y
    #     #     interploated.append(a)
    #     # result_sum = []
    #     # # Using zip and sum
    #     # for elements in zip(*interploated):
    #     #     result_sum.append(sum(elements)) 
    #     num_points = len(self.Time_Values)  # sample points
    #     z = 0
    #     for index in range(0, num_points):  # interpolation with sinc function
    #         z += self.Samples[index] * np.sinc((np.array(self.Time_Values) - (1/self.fs) * index) / (1/self.fs))

    #     self.gui.plot_widget_restored_signal.clear()
    #     self.gui.plot_widget_restored_signal.plot(self.time, z, pen="w")
    #     # self.gui.plot_widget_restored_signal.setYRange(-1,1)

    def Clear_Sig_Information(self):
        pass
    
    def Plot_Result_Signal(self):
        pass




    #-----------------------------------------------------------------------------------------------------------------------------#
    #                                                       Composer Methods                                                        #
    #-----------------------------------------------------------------------------------------------------------------------------#
    
    
    # Adds signal component to plot_widget_composed_signal
    def Add_Sig_Component(self):
        
        self.components_freq_adding()

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
                
        # Reset everything for next composition
        self.gui.plot_widget_composed.clear()
        self.gui.list_sig_components.clear()   
        self.composed_result.reset_resultant_sig()
        self.component_dict = {}
        print(len(self.composed_result.resultant_sig))


    # Exports the signal as a CSV file
    def Export_Composed_Signal_As_CSV(self):
        max_freq = (self.get_max_freq()) * 2
        self.composed_result.resultant_sig.append([max_freq])
        df = pd.DataFrame(self.composed_result.resultant_sig).transpose()
        df.columns = ['Time', 'Amplitude', 'F_Sampling']

        # Specify the base file path
        base_file_path = 'composed_signal_{}.csv'

        # Find the next available index for the filename
        index = 1
        while True:
            csv_file_path = base_file_path.format(index)
            try:
                # Try to open the file in 'x' mode to check if it exists
                with open(csv_file_path, 'x', newline=''):
                    # File doesn't exist, break the loop
                    break
            except FileExistsError:
                # File with this name already exists, try the next index
                index += 1

        # Open the file in 'w' mode, create a CSV writer object
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write data to the CSV file
            csv_writer.writerows([df.columns])  # Write column headers
            csv_writer.writerows(df.values)     # Write data rows

        print(f'CSV file "{csv_file_path}" created successfully with data in columns.')


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
