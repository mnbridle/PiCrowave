import copy
import os
import time
import numpy as np
from PIL import Image

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants
from wifi import test_data, spectral_data
import ui.spectral_plot


def spectral_demo(fb, spectral_data):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot

    timetrack = time.time()
    background_image_obj = Image.new("RGBA", fb.size, (0, 0, 0, 0))
    background_image_obj = ui.spectral_plot.initialise_image(background_image_obj, channel=1)
    print(f"Took {time.time() - timetrack} to generate the image")

    spectral_data.start()
    time.sleep(0.5)

    while(1):
        all_rf_data = []

        for channel in [1, 5, 9, 13]:
            spectral_data.change_channel(channel=channel)
            # Trigger the spectral scanner multiple times
            scan_count = 0
            while scan_count < 3:
                spectral_data.trigger_scan()
                scan_count += 1

        # Allow time for queues to be flushed
        timetrack = time.time()
        while not spectral_data.decoder_is_finished():
            time.sleep(0.05)
        print(f"Took {time.time() - timetrack} for the decoder to finish")

        while not spectral_data.queue_is_empty():
            _, rf_data = spectral_data.get_queue_data()
            all_rf_data.append(rf_data)

        timetrack = time.time()
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
    fb = Framebuffer(constants.framebuffer_number)
    wifi_rf = spectral_data.SpectralData()

    try:
        spectral_demo(fb, wifi_rf)
    except KeyboardInterrupt as e:
        wifi_rf.stop()

main()
