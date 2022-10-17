from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def main():
    fb = Framebuffer(constants.framebuffer_number)

    wifi_spectral_data = spectral_data.SpectralData()
    wifi_spectral_data.start()

    # Get test data
    while True:
        rf_data = test_data.full_spectrum_fft(min_freq=2400000, max_freq=2540000, freq_resolution=5000)
        print(rf_data)
        ui.spectral_plot.show_band(fb, rf_data)

main()