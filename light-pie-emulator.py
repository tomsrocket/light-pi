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
    size        = 32*5
    column      = bytearray( size * 3 + 1) # Whole strip in RGB 
    ledStrip    = bytearray( size * 3 + 1) # Whole strip in gamma corrected data, ready to be sent to spidev.
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

        # draw color test boxes
        #pygame.draw.rect(self.screen,(255,255,255),[10,10,10,10])
        #pygame.draw.rect(self.screen,(255,0,0),[30,10,10,10])


    def getSize(self):
        return self.size

    def show(self ):
        pygame.display.flip()
    #   spidev.write( self.ledStrip )
    #   spidev.flush()


    def setLedColor(self, y, color ):
        return self.setLedRgb( y, color[0], color[1], color[2] )

    def setLedRgb(self, y, r,g,b ):
        y3 = y * 3
        rr = int(r)
        rg = int(g)
        rb = int(b)
        if ( rr > 254):
            rr = 254
        if ( rg > 254):
            rg = 254
        if ( rb > 254):
            rb = 254
        if ( rr <0 ):
            rr=0
        if ( rg < 0 ):
            rg = 0
        if ( rb < 0 ):
            rb = 0

        self.ledStrip[y3 + 1] = self.gammaLookup[rr]
        self.ledStrip[y3]     = self.gammaLookup[rg]
        self.ledStrip[y3 + 2] = self.gammaLookup[rb]
        self.column[y3]   = rr
        self.column[y3+1] = rg
        self.column[y3+2] = rb

        pygame.draw.rect(self.screen,(rr,rg,rb),[y*6,20,5,5])



    def addLedColor( self, y, color ):
        y3 = y*3 
        rr = int(color[0])+self.column[y3+0]
        rg = int(color[1])+self.column[y3+1]
        rb = int(color[2])+self.column[y3+2]
        #logg( "set led color" + str(y) + ": (" + str(rr) + ", " + str(rg) + ", " + str(rb) )
        self.setLedRgb( y, rr,rg,rb )



class LedEffekts: 

    def cloud( self, ledStrip, size, pos, color ):  # size = pos => 0-100(%)
        stripSize = ledStrip.getSize();
        pixel = stripSize/100;
        mid = pos*pixel
        start = pos*pixel - size*pixel
        if ( start < 0 ):
            start = 0
        end =  pos*pixel + size*pixel
        if ( end > stripSize ) :
            end = stripSize
#        logg( "size " + str(size))pos*pixel
#        logg( "pos " + str(pos) )
        #logg( "range "  + str( start) + " - " + str(end ))
#        logg( "col "  + str( color[0]) + ", " + str(color[1] ) + ", " + str(color[2] ) )
        step = math.pi/ ( (end-start)  if (end-start) > 0.0001 else 0.0001 )
        for i in range(start,end):
            colo = self.decreaseColor( color,  math.sin( (i-start)*step) )
            ledStrip.addLedColor( i, colo )


    def decreaseColor( self, color, percentage ):
        if ( percentage > 1 ):
            percentage = percentage / 100
        pc =  percentage
        color  = ( color[0]*pc, color[1]*pc, color[2]*pc )
        return color





def sinLed( count, width ):
    return int( width+math.sin( count )*width )

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

LedStrip = LedStrip()
LedEffekts = LedEffekts();

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
        rr=0
        rg=0
        rb=0
        if (y + int(scroll)) % 30 == 0:
            rr=rg=int( 127+math.sin(inp)*127 )
            rb=0
#
#
        LedStrip.setLedRgb(y,  rr,rg,rb )



    LedEffekts.cloud( LedStrip, 30,sinLed( count *0.02, 70 ), (255,0,0) )
    LedEffekts.cloud( LedStrip, 60,sinLed( count *0.01, 70 ), (0,255,0) )
    LedEffekts.cloud( LedStrip, 40,sinLed( count *0.015, 70 ), (0,0,255) )


    # show the colors on LED strip & screen
    
    count=count+1
    LedStrip.show()
    time.sleep(0.01)
