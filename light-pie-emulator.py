#!/usr/bin/python

import math
import time
import pygame
#import sys




# logging 
def logg( msg):
    print msg;



#
# LedStrip
# Singleton class to control the LED strip
#
class LedStrip:
    column      = bytearray(32*5 * 3 + 1) # Whole strip in RGB 
    ledStrip    = bytearray(32*5 * 3 + 1) # Whole strip in gamma corrected data, ready to be sent to spidev.
    gammaLookup = bytearray(256)

    # singleton method
    def __call__(self):
        return self

    def __init__(self):
        logg( "Initializing LedStrip" )

        # Calculate gamma correction table.  This includes
        # LPD8806-specific conversion (7-bit color w/high bit set).
        for i in range(256):
            self.gammaLookup[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

        pygame.init() 
        self.screen = pygame.display.set_mode((640+161*2, 100)) 


    def show(self ):
        pygame.display.flip()
    #   spidev.write(column)
    #   spidev.flush()

    def setSingleColor(self, y, r,g,b ):
        y3 = y * 3
        rr = int(r)%255
        rg = int(g)%255
        rb = int(b)%255

        self.ledStrip[y3 + 1] = self.gammaLookup[rr]
        self.ledStrip[y3]     = self.gammaLookup[rg]
        self.ledStrip[y3 + 2] = self.gammaLookup[rb]
        self.column[y3 + 1] = rr
        self.column[y3]     = rg
        self.column[y3 + 2] = rb

        pygame.draw.rect(self.screen,(rr,rg,rb),[y*6,5,5,5])





def sinLed( count ):
    return int( 127+math.sin( count )*127 )

def sinCake( count, width ):
    logg( int( 127+math.sin( count )*127  ) )



# how many LEDs do we have
width     = 32*5
column = bytearray(32*5 * 3 + 1)


# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."


count =0
rs = 255
gs = 0
bs = 0
scroll = 0


while True:
    rs=(rs-0.5)%255
    bs=(bs+1)%255
    scroll = scroll + 0.25
    inp = count/100.0%(2*math.pi);

    r = rs
    b = bs
    g = gs
    for y in range(width):
        b=b+1
        r=r-1






        # save current LED color
        rr=r
        rg=g
        rb=b
        if (y + int(scroll)) % 30 == 0:
            rr=rg=int( 127+math.sin(inp)*127 )
            rb=0

        LedStrip.setSingleColor(y,  rr,rg,rb )




    # show the colors on LED strip & screen
    sinLed( count  )
    count=count+1
    LedStrip.show()
    time.sleep(0.01)
