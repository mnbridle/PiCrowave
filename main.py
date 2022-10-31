import numpy as np

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def spectral_demo(fb, spectral_data, avg_count = 100):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot
    image_data = ui.spectral_plot.initialise_image()

    while(1):
        print("Any data?")
        rf_data = spectral_data.get_queue_data()
        ui.spectral_plot.show_band(fb, rf_data, image_data)

def main():
    fb = Framebuffer(constants.framebuffer_number)

    wifi_rf = spectral_data.SpectralData()
    wifi_rf.start(channel=1)

    try:
        spectral_demo(fb, wifi_rf, avg_count = 200)
    except KeyboardInterrupt as e:
        wifi_rf.stop()

main()
