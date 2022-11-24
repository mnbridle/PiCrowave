import copy
import os
import time
import numpy as np

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def spectral_demo(fb, spectral_data, channel):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot

    timetrack = time.time()
    image_data = copy.copy(ui.spectral_plot.initialise_image(fb, channel=channel))
    print(f"Took {time.time() - timetrack} to generate the image")

    old_fb = copy.copy(fb)

    while(1):
        timetrack = time.time()
        start_time = time.time()
        while time.time() - start_time < 0.25:
            time.sleep(0.05)

        print(f"Waited for {time.time() - timetrack}")

        timetrack = time.time()
        rf_data = spectral_data.get_queue_data()
        print(f"Time to get RF data: {time.time() - timetrack}")

        timetrack = time.time()
        new_fb = copy.copy(old_fb)
        ui.spectral_plot.show_band(new_fb, rf_data, image_data)
        print(f"Took {time.time() - timetrack} to plot the image")

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
