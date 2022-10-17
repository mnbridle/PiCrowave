from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def main():
    fb = Framebuffer(constants.framebuffer_number)

    # Get test data
    while True:
        spectral_data.live_sample()
        rf_data = test_data.full_spectrum_fft(min_freq=2400000, max_freq=2540000, freq_resolution=5000)
        ui.spectral_plot.show_band(fb, rf_data)

main()