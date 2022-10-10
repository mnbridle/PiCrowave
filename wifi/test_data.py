import math
import numpy as np

def full_spectrum_fft(min_freq=2400000, max_freq=2483500, min_power=-96, max_power=-30):
    # Generate full-spectrum FFT data, from 2400 to 2483.5MHz, data points every 312.5kHz
    frequencies = np.arange(min_freq, max_freq, 312.5)
    rssi = np.random.randint(low=min_power, high=max_power, size=(frequencies.size))

    data = np.dstack((frequencies, rssi))
    data = np.squeeze(data)
    
    return data