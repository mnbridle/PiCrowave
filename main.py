from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data

import ui.spectral_plot


def main():
    fb = Framebuffer(constants.framebuffer_number)

    # Get test data
    rf_data = test_data.full_spectrum_fft()
    ui.spectral_plot.show_band(fb, rf_data)

main()