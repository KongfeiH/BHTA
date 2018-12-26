# Ex05a.py
#
# Supplemental helper file for Ex05. More advanced parsing techniques are used
# in this file, but it is nonetheless still fairly simple. This file is mostly
# to avoid clutter and not force unneeded technical details on anyone who does
# not have any want or need to read them.

# The ROLE property is a special property in that its bits encode quite a bit 
# of information. The specifics are outlined online (link below).
# http://web.barrett.com/support/Puck_Documentation/RoleProperty.pdf
# In essence, the role is held in a 16-bit number: 0ABC DEFG HI00 JJJJ
# Each letter corresponds to a bit, which in turn corresponds to features of 
# the motor controller.
# A - Optical Encoder				# F - Hall Motor Encoder
# B - IMU for Force-Torque Sensor	# G - Digital/Serial Motor Encoder
# C - Tactile Sensors				# H - 20 MHz (vs 32 MHz)
# D - Strain Gauges					# I - Internal Thermistor Bit
# E - Enc Motor Encoder				# J - 4-bit Product Identifier
def parse_role(role):
	detailed_role = str()

	# Firstly, what kind of product is this?
	product_identifier = role & 0xF
	if product_identifier == 0:
		detailed_role += 'Product: WAM Puck\n'
	elif product_identifier == 1 or product_identifier == 4:
		detailed_role += 'Product: Undefined\n'
		raise Exception("Undefined Puck Product Identifier")
	elif product_identifier == 2:
		detailed_role += 'Product: Safety Puck\n'
	elif product_identifier == 5:
		detailed_role += 'Product: BHand Puck\n'
		# In this program, this is the most likely case scenario.
	elif product_identifier == 6:
		detailed_role += 'Product: F/T Sensor\n'

	detailed_role += 'Extras: '
	# What commodities does this have?
	if role & 0x40:
		detailed_role += 'Internal Thermistor, '
	if role & 0x80:
		detailed_role += '20 MHz crystal, '
	else:
		detailed_role += '32 MHz crystal, '
	if role & 0x100:
		detailed_role += 'Digital/Serial Motor Encoder, '
	if role & 0x200:
		detailed_role += 'Hall Motor Encoder, '
	if role & 0x400:
		detailed_role += 'Enc Motor Encoder, '
	if role & 0x800:
		detailed_role += 'Strain Gauge, '
	if role & 0x1000:
		detailed_role += 'Tactile Sensors, '
	if role & 0x2000:
		detailed_role += 'IMU for Force-Torque Sensor, '
	if role & 0x4000:
		detailed_role += 'Optical Encoder'

	return detailed_role


# The MODE property is fundamentally much simpler than the ROLE property. It 
# contains a mere integer between 0 and 5 (excluding 1). Each of those 
# corresponds to a mode of the puck.
def parse_mode(mode):
	if mode == 0:
		return "IDLE"
	if mode == 2:
		return "TORQUE"
	if mode == 3:
		return "PID"
	if mode == 4:
		return "VEL"
	if mode == 5:
		return "TRAP"
	raise Exception("Invalid Mode: "+str(mode))