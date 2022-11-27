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
        all_rf_data = []

        for channel in [1, 5, 9, 13]:
            spectral_data.change_channel(channel=channel)
            time.sleep(0.25)

        spectral_data.pause()

        timetrack = time.time()
        # Process the data
        while spectral_data.queue_is_empty():
            _, rf_data = spectral_data.get_queue_data()
            all_rf_data.append(rf_data)

        # Get data frame
        data_frame = np.concatenate((all_rf_data), axis=0)
        sorted_data_frame = data_frame[data_frame[:, 0].argsort()]

        freq_dict = {}
        for data in sorted_data_frame:
            if data[0] not in freq_dict:
                freq_dict[data[0]] = [data[1]]
            else:
                freq_dict[data[0]].append(data[1])

        # Get maximum RSSI for sample period
        max_power_per_freq = []
        for freq in freq_dict:
            max_power_per_freq.append((freq, max(freq_dict[freq])))

        full_frame = np.array(max_power_per_freq)
        print(f"Took {time.time() - timetrack} to process the RF data")

        timetrack = time.time()
        graph_image_obj = Image.new("RGBA", fb.size, (0, 0, 0, 0))
        graph_image_obj = ui.spectral_plot.show_band(graph_image_obj, full_frame)
        print(f"Took {time.time() - timetrack} to plot the image")

        # Write to framebuffer
        new_img = Image.blend(background_image_obj, graph_image_obj, 0.5)
        fb.show(new_img)


def main():
    channel = 1
    fb = Framebuffer(constants.framebuffer_number)

    wifi_rf = spectral_data.SpectralData()
    wifi_rf.start(channel=channel)

    try:
        spectral_demo(fb, wifi_rf, channel)
    except KeyboardInterrupt as e:
        wifi_rf.stop()

main()
