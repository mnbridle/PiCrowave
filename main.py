import numpy as np

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def main():
    fb = Framebuffer(constants.framebuffer_number)

    wifi_spectral_data = spectral_data.SpectralData()
    wifi_spectral_data.start(channel=1)

    # Get test data
    work_queue = wifi_spectral_data.get_work_queue()

    while True:
        try:
            print("Getting data")
            (ts, (tsf, freq, noise, rssi, pwr)) = work_queue.get(block=True)
            print(ts)
            rf_data = np.array(list(pwr.items()))
            ui.spectral_plot.show_band(fb, rf_data)
        except KeyboardInterrupt as e:
            wifi_spectral_data.stop()
            break

main()