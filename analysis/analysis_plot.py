from data import LidarDataClient
import configparser
import matplotlib.pyplot as plt
import math
import os
import time
import sys

# Read config file:
config = configparser.ConfigParser()
config.read('config/config.ini')

try:
    HOST = config['Dataserver']['Host']         # The remote host
    PORT = int(config['Dataserver']['Port'])    # The same port as used by the server
except KeyError:
    print("ERROR: Please create 'example.ini' in config directory, based on the provided example.")
    sys.exit(1)

# Create figure:
fig1 = plt.figure(1)

# Clear figure:
plt.clf()

# Enable interactive mode:
plt.ion()

# Create polar subplot:
sbp = plt.subplot(111)

sbp.autoscale(True)

# Create axis:
ax = fig1.add_axes(sbp)

# Set radius limit:
ax.set_ylim(ymin=-100, ymax=500)
ax.set_xlim(xmin=-400, xmax=400)


def unzip_catch(d):
    try:
        x, y = zip(*d)
    except ValueError:
        x = y = []
    return x, y

if __name__ == "__main__":
    with LidarDataClient(HOST, PORT) as s:
        # Initial plot:
        plt.plot([0], [0], marker='.', color='black')
        wnt_pts, = plt.plot([], [], lw=1, marker='+', color='r')
        otr_pts, = plt.plot([], [], lw=1, marker='+', color='b')

        while True:
            # Update plot data:
            d = s.data
            wnt_x, wnt_y = unzip_catch(d['sweep_wnt'])
            otr_x, otr_y = unzip_catch(d['sweep_otr'])

            wnt_pts.set_xdata(wnt_x)
            wnt_pts.set_ydata(wnt_y)
            otr_pts.set_xdata(otr_x)
            otr_pts.set_ydata(otr_y)

            # Draw new plot:
            plt.draw()

            # Pause for plot update:
            plt.pause(0.01)
