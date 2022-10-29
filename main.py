import numpy as np

from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

from wifi import test_data, spectral_data

import ui.spectral_plot


def spectral_demo(fb, spectral_data, avg_count = 100):
    # This will need to be fast
    # Get the data, average the samples, pump out a plot
    while(1):
        count = 0
        cuml_rf_data = None
        while count < avg_count:
            # Add things together
            (_, (_, _, _, _, pwr)) = spectral_data.get_queue_data()
            rf_data = np.array(list(pwr.items()))

            if cuml_rf_data is None:
                cuml_rf_data = rf_data
            else:
                cuml_rf_data[:, 1] += rf_data[:, 1]
            count += 1

        
        cuml_rf_data[:, 1] = cuml_rf_data[:, 1] / count
        ui.spectral_plot.show_band(fb, cuml_rf_data)


def main():
    fb = Framebuffer(constants.framebuffer_number)

    wifi_spectral_data = spectral_data.SpectralData()
    wifi_spectral_data.start(channel=1)

    try:
        spectral_demo(fb, spectral_data)
    except KeyboardInterrupt as e:
        wifi_spectral_data.stop()

main()