from .athspectralscan import AthSpectralScanner, DataHub,  AthSpectralScanDecoder
import wifi.constants
import multiprocessing as mp
import numpy as np
import queue
import logging
import time
import sys
import os

class SpectralData(object):
    def __init__(self):
        self._setup_logging()
        self.output_queue = mp.Queue()

        # Setup decoder
        self.decoder = AthSpectralScanDecoder()
        self.decoder.set_number_of_processes(8)  # so we do not need to sort the results by TSF
        self.decoder.set_output_queue(self.output_queue)
        self.decoder.disable_pwr_decoding(False)

        self.decoder.start()

        # Setup scanner and data hub
        self.scanner = AthSpectralScanner(interface=wifi.constants.interface)
        self.hub = DataHub(scanner=self.scanner, decoder=self.decoder)

    def start(self):
        self.scanner.set_spectral_short_repeat(1)
        self.scanner.set_mode("manual", skip_interface_config=False)
        self.scanner.set_spectral_count(127)

        self.hub.start()
        self.scanner.start()

    def change_channel(self, channel):
        self.scanner.set_channel(channel)

    def trigger_scan(self):
        self.scanner.trigger()

    def stop(self):
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

    def get_queue_data(self):
        return self.output_queue.get(block=True)

    def queue_is_empty(self):
        return self.output_queue.empty()

    def decoder_is_finished(self):
        return self.decoder.is_finished()

