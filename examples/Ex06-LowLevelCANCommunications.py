# Ex06-LowLevelCANCommunications
#
# In the following examples, I will go through how to use low level CAN 
# messages to send binaries to and recieve them from the hand. Much of what is
# covered here is described in detail in the following document:
# http://web.barrett.com/support/Puck_Documentation/CAN_Message_Format.pdf
#

import time
import sys
sys.path.append('../pyHand/pyHand_API')
from pyHand_api import initialize, write_msg, read_msg, can_reset, can_uninit
from puck_properties_consts import *

# As always, we need to initialize CAN communications.
initialize()

# The following function gets the raw CAN data when querying for a property's
# value through the CAN.
def get_raw_can_frame(to_motor, prop):
	# First, clear the CAN of any unwanted data.
	can_reset()

	# The CAN sends an array of up to 8 values to the hand.
	# This payload is typically 1, 4, or 6 values long, with a few exceptions.
	write_msg(to_motor, [prop])

	# Now we read back from the CAN.
	read_in = read_msg()
	# read_msg returns a tuple of three values.
	# A TPCANStatus object. This can be treated as an int, and essentially 
	#	serves as an error code for messages sent along th CAN.
	# A TPCANMsg object. Has the following fields: ID, MSGTYPE, LEN, DATA.
	#	The purposes of these fields are explained in detail in the document 
	#	linked to at the top of this file.
	# A TPCANTimestamp object. Not really relevant to anything we do.

	message_in = read_in[1] # The TPCANMsg.
	data = message_in.DATA # This is just an array of c_ubytes from ctypes.
	length = message_in.LEN # Length of data payload

	# Just printing to the screen.
	datastring = ""
	for i in range(length):
		datastring += hex(data[i])+"\t"
	return datastring

# You can replace the properties below with any constants from the property
# list online. If you do not look at the documentation that I keep dropping
# links to, you will not understand how to program effectively for the 
# BarrettHand. These examples are merely secondary.
# http://web.barrett.com/support/Puck_Documentation/PuckProperties-r200.pdf

# Feel free to play around with this code. The easiest way to learn is by just
# messing with it.

print "Max Torque:  ", get_raw_can_frame(FINGER1, MT)
print "Temperature: ", get_raw_can_frame(FINGER1, TEMP)
print "Close Target:", get_raw_can_frame(FINGER1, CT)

# Looking at those frames, you may be wondering how you interpret this data. 
# All you see are a bunch of hex codes that don't seem to mean much. They are 
# not even the same length, so how do we parse this?
# Note that for most properties, this function is redundant. In the pyHand api,
# the get_property method would be sufficient. This is for purely demonstrative
# purposes.

def parse_raw_can_frame(to_motor, prop):
	# Just as before, we get the read data.
	write_msg(to_motor, [prop])
	read_in = read_msg()
	message_in = read_in[1]
	data = message_in.DATA
	# Important note: data[0] contains a 'set' bit, and the property number 
	#	from which this data is retrieved. For example, if data[0] contains
	#	0xab, then it refers to 'set' property 0x2b, which is MT.
	# 	Unfortunately, this method does not utilize that fact. However, this is
	# 	incredibly useful when writing your own functions.
	# data[1] is typically empty except in some special cases, such as position
	#	data collection and tactile data collection.

	# Look at the CAN Message Format file for a clear explanation of what is 
	# going on below.
	# Essentially, we are adding together the bytes in a meaningful manner.
	val = 0
	try:
		# Check to see if the data is a 32-bit property
		val = val*0x100 + data[5]
		val = val*0x100 + data[4]
		val = val*0x100 + data[3]
		val = val*0x100 + data[2]
	except:
		# If there is no data[5] or data[4] byte, then we interpret this as a
		# 16 bit property.
		val = val*0x100 + data[3]
		val = val*0x100 + data[2]
	return val

mt = parse_raw_can_frame(FINGER1, MT)
print "\nMax Torque:   ", mt
temp = parse_raw_can_frame(FINGER1, TEMP)
print "Temperature:  " , temp
ct = parse_raw_can_frame(FINGER1, CT)
print "Close Target: " , ct

# Now we know how to read properties from the hand, but how do we set those?
def set_raw_property(motor, prop, value):
	msg_out = [0,0,0,0,0,0]
	#The first bit in the first byte tells the motor to 'set' a property. 
	msg_out[0] = 0x80 | prop
	msg_out[1] = 0 #no data here
	msg_out[2] = (value >> 0) & 0xFF
	msg_out[3] = (value >> 8) & 0xFF
	msg_out[4] = (value >> 16) & 0xFF
	msg_out[5] = (value >> 24) & 0xFF

	if msg_out[4]==0 and msg_out[5]==0:
		# This may be a 16 bit property.
		msg_out = msg_out[0:4]

	write_msg(motor, msg_out)

	# Returning the string of data values so that it's clear what is happening
	# behind the scenes.
	datastring = ""
	for i in range(len(msg_out)):
		datastring += hex(msg_out[i])+"\t"
	datastring += "\nProperty "+str(prop)+" set to "+str(value)
	return datastring

print "\nMax Torque:   ", set_raw_property(FINGER1, MT, 2000)
print "Temperature:  " , set_raw_property(FINGER1, TEMP, 10)
print "Close Target: " , set_raw_property(FINGER1, CT, 180000)

# However, it makes no sense to set the temperature around the puck. Therefore,
# some properties cannot actually be set. To demonstrate this, we now print 
# these properties out again.

print "\nMax Torque:   ",parse_raw_can_frame(FINGER1, MT)
print "Temperature:  " , parse_raw_can_frame(FINGER1, TEMP)
print "Close Target: " , parse_raw_can_frame(FINGER1, CT)

# Lastly, let's set these back to their initial values.
print "\nMax Torque:   ", set_raw_property(FINGER1, MT, mt)
print "Temperature:  " , set_raw_property(FINGER1, TEMP, temp)
print "Close Target: " , set_raw_property(FINGER1, CT, ct)

can_uninit()