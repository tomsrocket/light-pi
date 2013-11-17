#!/usr/bin/python

import time
import pygame
#import sys


pygame.init() 
screen = pygame.display.set_mode((640+161*2, 100)) 


def ledColor( screen, led, r, g, b ):
	pygame.draw.rect(screen,(int(r)%255,int(g)%255,int(b)%255),[led*6,5,5,5])

# how many LEDs do we have
width     = 32*5

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
	gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)


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






		# save current LED color
		rr=r
		rg=g
		rb=b
		if (y + int(scroll)) % 10 < 2:
			rr=rg=int(rs)
			rb=0

		ledColor(screen, y,rr,rg,rb)
		column[y3 + 1] = gamma[int(rr)%255]
		column[y3]     = gamma[int(rg)%255]
		column[y3 + 2] = gamma[int(rb)%255]


	# show the colors on LED strip & screen
	pygame.display.flip()
#	spidev.write(column)
#	spidev.flush()
	time.sleep(0.005)
