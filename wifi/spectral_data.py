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

        self.work_queue = mp.Queue()
        self.output_queue = mp.Queue()

        # Setup decoder
        self.decoder = AthSpectralScanDecoder()
        self.decoder.set_number_of_processes(8)  # so we do not need to sort the results by TSF
        self.decoder.set_output_queue(self.work_queue)
        self.decoder.disable_pwr_decoding(False)

        self.decoder.start()

        # Setup scanner and data hub
        self.scanner = AthSpectralScanner(interface=wifi.constants.interface)
        self.hub = DataHub(scanner=self.scanner, decoder=self.decoder)

    def start(self, channel=1):
        self.scanner.set_spectral_short_repeat(0)
        self.scanner.set_mode("background")
        self.scanner.set_channel(channel)

        self.hub.start()
        self.scanner.start()

    def change_channel(self, channel):
        self.scanner.stop()
        self.scanner.set_mode("background")
        self.scanner.set_channel(channel)
        self.scanner.start()

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

    def get_work_queue(self):
        return self.work_queue

    def get_queue_data(self):
        return self.work_queue.get(block=True)

    def get_queue_size(self):
        return self.work_queue.qsize()

    def clear_queue(self):
        while not self.work_queue.empty():
            self.work_queue.get()
        print("Queue emptied")
