from sweeppy import Sweep
from dagurs039 import DaguRS039
from .data import dataserver
import math
import os
import threading


class LidarTankPlatform:
    DEV = os.environ['SCANSE_SWEEP_PORT']
    WIDTH = 30.
    FORWARD = 100.

    # Create lists:
    analysis_data = dataserver.analysis_data

    def __init__(self, *args, **kwargs):
        self.sweep = None
        self.motors = DaguRS039(*args, **kwargs)

        self._running = None

        self.st = threading.Thread(target=self._sweep_data_helper)
        self.ds = None  # Data socket server
        self.dst = None  # Data socket server thread

    def __enter__(self):
        self._running = True

        # Start sweep thread
        self.sweep = Sweep(self.DEV).__enter__()
        self.sweep.start_scanning()
        self.st.start()  # Start Sweep thread

        # Data server:
        self.ds, self.dst = dataserver.start()  # Start data server, and store socket server and thread objects
        return self

    def __exit__(self, *args, **kwargs):
        self._running = False

        # Sweep close
        self.st.join()  # Wait Sweep thread to end
        self.sweep.__exit__(*args, **kwargs)

        # Data server:
        self.ds.close()  # Close socket server
        self.dst.join()  # Wait for loop thread to close

    # Gets data from sweep:
    def _sweep_data_helper(self):
        for scan in self.sweep.get_scans():
            if not self._running:
                return

            tmp_sweep_wnt = []
            tmp_sweep_otr = []
            for smp in scan.samples:
                a = (((smp.angle / 1000) + 135) % 360) * (math.pi / 180)
                d = smp.distance  # cm

                cart_p = [math.cos(a) * d, math.sin(a) * d]

                if -self.WIDTH / 2. < cart_p[0] < self.WIDTH / 2. and 0. < cart_p[1] < self.FORWARD:
                    tmp_sweep_wnt.append([cart_p[0], cart_p[1]])
                    # print("conn: {}, d: {}, x: {}, y: {}".format(conn, d, cart_p[0], cart_p[1]))
                else:
                    tmp_sweep_otr.append([cart_p[0], cart_p[1]])

            self.analysis_data['sweep_wnt'] = tmp_sweep_wnt
            self.analysis_data['sweep_otr'] = tmp_sweep_otr
