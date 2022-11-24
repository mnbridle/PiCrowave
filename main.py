import copy
import os
import time
import numpy as np
from PIL import Image

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants
from wifi import test_data, spectral_data
import ui.spectral_plot


def spectral_demo(fb, spectral_data, channel):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot

    timetrack = time.time()

    background_image_obj = Image.new("RGBA", fb.size, (0, 0, 0, 0))
    background_image_obj = ui.spectral_plot.initialise_image(background_image_obj, channel=channel)

    print(f"Took {time.time() - timetrack} to generate the image")

    while(1):
        timetrack = time.time()
        ts, rf_data = spectral_data.get_queue_data()
        print(f"Time to get RF data: {time.time() - timetrack}")

        print(f"Timestamp: {ts}")

        timetrack = time.time()
        graph_image_obj = Image.new("RGBA", fb.size, (0, 0, 0, 0))
        graph_image_obj = ui.spectral_plot.show_band(graph_image_obj, rf_data)

        print(f"Took {time.time() - timetrack} to plot the image")

        # Write to framebuffer
        new_img = Image.blend(background_image_obj, graph_image_obj, 0.5)
        fb.show(new_img)

        # Change channel
        channel += 1
        channel %= 14

        timetrack = time.time()
        print(f"Change to channel {channel+1}")
        spectral_data.change_channel(channel=channel+1)
        print(f"Took {time.time() - timetrack} to change channel")


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
