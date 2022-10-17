from .athspectralscan import AthSpectralScanner, DataHub,  AthSpectralScanDecoder
import multiprocessing as mp
import queue
import logging
import time
import sys
import os

def live_sample():
    interface = "wlan1"

    # Setup logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    # Setup a queue to store the result
    work_queue = mp.Queue()
    decoder = AthSpectralScanDecoder()
    decoder.set_number_of_processes(1)  # so we do not need to sort the results by TSF
    decoder.set_output_queue(work_queue)
    decoder.disable_pwr_decoding(True)   # enable to extract "metadata": time (TSF), frequency, etc  (much faster!)
    decoder.start()

    # Setup scanner and data hub
    scanner = AthSpectralScanner(interface=interface)
    hub = DataHub(scanner=scanner, decoder=decoder)

    #scanner.set_mode("chanscan")
    scanner.set_spectral_short_repeat(1)
    scanner.set_mode("background")
    scanner.set_channel(1)


    # Start to read from spectral_scan0
    hub.start()
    # Start to acquire dara
    scanner.start()
    logger.info("Collect data for 10 seconds")

    start_time = time.time()

    while time.time() - start_time < 10:
        (ts, (tsf, freq, noise, rssi, pwr)) = work_queue.get(block=True)
        print(ts, tsf, freq, noise, rssi, pwr)

    # Tear down hardware
    scanner.stop()
    hub.stop()