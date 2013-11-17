#!/usr/bin/python

# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

import RPi.GPIO as GPIO, Image, time
import sys

test      = sys.argv[1]
print "Filename is " + test

# Configurable values
filename  = test
dev       = "/dev/spidev0.0"

# Open SPI device, load image in RGB format and get dimensions:
spidev    = file(dev, "wb")
width     = 32*5

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
	gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

# Create list of bytearrays, one for each column of image.
# R, G, B byte per pixel, plus extra '0' byte at end for latch.
#print "Allocating..."
#column = [0 for x in range(width)]
#column = bytearray(width * 3 + 1)

# Convert 8-bit RGB image into column-wise GRB bytearray list.


# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."
column = bytearray(width * 3 + 1)
rs = 255
gs = 0
bs = 0
scroll = 0
while True:
	rs=(rs-0.5)%255
	bs=(bs+1)%255
	scroll = scroll + 0.25

	r = rs
	b = bs
	g = gs
	for y in range(width):
		y3 = y * 3
		b=b+1
		r=r-1
		if (y + int(scroll)) % 10 < 2:
			column[y3+1]     = gamma[int(rs)] # red
			column[y3]       = gamma[int(rs)] # green 
			column[y3+2]     = gamma[0] # blue
		else:
			column[y3 + 1] = gamma[int(r)%255]
			column[y3]     = gamma[int(g)%255]
			column[y3 + 2] = gamma[int(b)%255]

	spidev.write(column)
	spidev.flush()
	time.sleep(0.005)
