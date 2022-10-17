from .athspectralscan import AthSpectralScanner, DataHub,  AthSpectralScanDecoder
import .wifi.constants
import multiprocessing as mp
import queue
import logging
import time
import sys
import os

class SpectralData(object):
    def __init__(self):
        self._setup_logging()

        self.work_queue = mp.Queue()
        self.output_queue = mp.Queue()

        # Setup decoder
        self.decoder = AthSpectralScanDecoder()
        self.decoder.set_number_of_processes(1)  # so we do not need to sort the results by TSF
        self.decoder.set_output_queue(self.work_queue)
        self.decoder.disable_pwr_decoding(False)

        self.decoder.start()

        # Setup scanner and data hub
        self.scanner = AthSpectralScanner(interface=wifi.constants.interface)
        self.hub = DataHub(scanner=self.scanner, decoder=self.decoder)

    def start(self):
        #scanner.set_mode("chanscan")
        self.scanner.set_spectral_short_repeat(1)
        self.scanner.set_mode("background")
        self.scanner.set_channel(1)

        self.hub.start()
        self.scanner.start()

        self.logger.info("Collect data for 10 seconds")

        start_time = time.time()

        while time.time() - start_time < 10:
            (ts, (tsf, freq, noise, rssi, pwr)) = self.work_queue.get(block=True)
            print(ts, tsf, freq, noise, rssi, pwr)

        # Tear down hardware
        self.scanner.stop()
        self.hub.stop()

    def _setup_logging(self):
        # Setup logger
        self.logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def get_output_queue(self):
        return self.output_queue
