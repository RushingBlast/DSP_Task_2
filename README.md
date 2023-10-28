# Sampling Studio App

The Sampling Studio app is a signal processing tool that allows users to load signals, visualize and sample them at different frequencies, recover the original signal using the sampled points, and perform various operations on the signals. This README file provides an overview of the app's features and instructions on how to use them effectively.

## Features

The Sampling Studio app offers the following key features:

1. **Signal Loading**: Users can load signals from external files to analyze and process.

2. **Signal Visualization**: The app provides three graphs for signal visualization:
   - The first graph displays the original signal along with markers indicating the sampled points.
   - The second graph displays the reconstructed signal based on the sampled points.
   - The third graph shows the difference between the original and reconstructed signals.

3. **Signal Sampling**: Users can sample the loaded signal at different frequencies and adjust the sampling rate.

4. **Signal Recovery**: The app allows users to reconstruct the original signal using the sampled points.

5. **Signal Composer**: Users can compose signals by adding multiple sinusoidal components with different frequencies and magnitudes.

6. **Component Removal**: Users can remove specific components from the mixed signal during the composition process.

7. **Noise Addition**: Users can add noise to the loaded signal with a custom Signal-to-Noise Ratio (SNR) level for further analysis.

## Getting Started

To use the Sampling Studio app, follow these steps:

1. Run the app by executing the Sample_Studio.py file.

2. The app's graphical user interface (GUI) will appear, providing various options and controls for signal processing.

## Usage

1. **Load a Signal**: Click on the "Open Signal" button to load a signal from an external file. Supported file format CSV. The loaded signal will be displayed in the first graph.

2. **Signal Sampling**: Adjust the sampling frequency by the frequency slider. The sampled points will be displayed as markers on the first graph.

3. **Signal Recovery**: The reconstructed signal will be displayed in the second graph when the user changes the sampling frequency.

4. **Signal Comparison**: The third graph displays the difference between the original signal and the reconstructed signal.

5. **Signal Composer**: Use the "Signal Composer" section to compose signals. Add sinusoidal components with different frequencies and magnitudes to create a mixed signal. Adjust the parameters and click on the "Add Component" button to generate the mixed signal. The component will be displayed in the “Component Preview” graph and the composed signal will be displayed in the “Composed Signal Preview” graph.

6. **Component Removal**: If necessary, select specific components from the mixed signal in the "Component List" list  and click on the "Remove Component" button to remove them. The modified mixed signal will be displayed in the “Composed Signal Preview” graph.

7. **Noise Addition**: In the "Signal Viewer" section, adjust the SNR level slider to add noise to the loaded or composed signal. The noisy signal will be displayed in the first graph.

8. **Exporting**: The app allows you to export the composed signals for further analysis when the user clicked on “Save Composed Signal” button. Use the provided export options to save the signals in csv file format.
