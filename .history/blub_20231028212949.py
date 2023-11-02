import numpy as np
from scipy.interpolate import CubicSpline
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from PyQt5.QtWidgets import QApplication

# Original signal
x = np.linspace(0, 10, 100)  # Time values
y = np.sin(x)  # Original signal

# Generate noisy signal (for demonstration purposes)
noise = np.random.normal(0, 0.1, len(y))
noisy_signal = y + noise

# Cubic spline interpolation
cs = CubicSpline(x, noisy_signal)

# Reconstruct the signal
reconstructed_signal = cs(x)

# Create an application instance
app = QApplication([])

# Create a plot widget
plot_widget = pg.plot(title='Signal Reconstruction using Cubic Spline Interpolation')

plot_widget.addLegend()
# Plot the original signal
plot_widget.plot(x, y, pen='b', name='Original Signal')

# Plot the noisy signal
plot_widget.plot(x, noisy_signal, pen='r', name='Noisy Signal')

# Plot the reconstructed signal
plot_widget.plot(x, reconstructed_signal, pen='g', name='Reconstructed Signal')
# Run the application event loop
app.exec_()