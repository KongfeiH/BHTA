# force_torque_data_export.py
#
# Exports data from the force/torque sensor to an output file.

import time
import sys
from ftsstr import ftsstr
import pyHand_API.pyHand_api as bt

FTS_ID = 8
bt.initialize()

def write_line(sensor, file_out):
    try:
        sensor.update()
    except:
        write_line(sensor, file_out)

    file_out.write(str(sensor.forceX)+', ')
    file_out.write(str(sensor.forceY)+', ')
    file_out.write(str(sensor.forceZ)+', ')
    file_out.write(str(sensor.torqueX)+', ')
    file_out.write(str(sensor.torqueY)+', ')
    file_out.write(str(sensor.torqueZ)+'\n')

if bt.get_property(FTS_ID, 1):
    print "Export data from the Barrett Technology Force/Torque Sensor."
    print "By default, the data will be exported to the current directory as a .csv."
    filename = raw_input("Filename: ")
    print "Please allow about .2 seconds per frame frames."
    cycles = int(raw_input("Number of Frames to Collect: "))

    filename = filename+'.csv'
    file_out = open(filename, 'w+')
    sensor = ftsstr()

    file_out.write('Fx, Fy, Fz, Tx, Ty, Tz\n')

    sys.stdout.write('|') # Begin progress bar.
    for i in range(cycles):
        write_line(sensor, file_out)
        sys.stdout.write('*')
        time.sleep(.2)

    sys.stdout.write('|\n')
    print "Export Complete."
    file_out.close()

else:
    print "No Force/Torque Sensor to read data from."