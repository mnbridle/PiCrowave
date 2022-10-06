import math
import numpy as np

def full_spectrum_fft():
    # Generate full-spectrum FFT data, from 2400 to 2483.5MHz, data points every 312.5kHz
    frequencies = np.arange(2400000, 2483500, 312.5)
    rssi = np.random.randint(low=-96, high=-30, size=(frequencies.size))

    data = np.dstack((frequencies, rssi))
    data = np.squeeze(data)
    
    return data