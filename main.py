import numpy as np

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def spectral_demo(fb, spectral_data, channel):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot

    while(1):
        rf_data = spectral_data.get_queue_data()
        image_data = ui.spectral_plot.initialise_image(fb, channel=channel)
        ui.spectral_plot.show_band(fb, rf_data, image_data)

def main():
    channel = 7
    fb = Framebuffer(constants.framebuffer_number)

    wifi_rf = spectral_data.SpectralData()
    wifi_rf.start(channel=channel)

    try:
        spectral_demo(fb, wifi_rf, channel)
    except KeyboardInterrupt as e:
        wifi_rf.stop()

main()
