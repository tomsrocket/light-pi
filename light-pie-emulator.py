#!/usr/bin/python

import math
import time
import pygame
#import sys




# logging 
def logg( msg):
    print msg;

SIZE = 32*5

#
# LedStrip
# Singleton class to control the LED strip
#
class LedStrip:
    size        = SIZE
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


    def sanitizeColor( self, c ):
        sc = int(c)
        if ( sc > 254):
            sc = 254
        if ( sc < 0):
            sc = 0
        return sc


    def show( *args  ):
        self = args[0]
        leds = self.ledStrip
        cols = self.column
#        def lookupSum( a, b ): 
#       TODO: calculate the sum of ledstrip and add

        if ( len(args)>1 and args[1] != None ):
            add = args[1]
            cols = map(lambda x, y : x + y, self.column, add)

        if ( len(args)>2 and args[2] != None ):
            print "subbing"
            sub = args[2]
            cols = map(lambda x, y : x - y, self.column, sub)

        for y in range(self.size):
            y3=y*3
            rr = self.sanitizeColor(cols[y3+0] )
            rg = self.sanitizeColor(cols[y3+1] )
            rb = self.sanitizeColor(cols[y3+2] )
            pygame.draw.rect(self.screen,(rr,rg,rb),[y*6,20,5,5])
        
        pygame.display.flip()


    #   spidev.write( self.ledStrip )
    #   spidev.flush()


    def setLedColor(self, y, color ):
        return self.setLedRgb( y, color[0], color[1], color[2] )

    def setLedRgb(self, y, r,g,b ):
        y3 = y * 3
        rr = self.sanitizeColor(r)
        rg = self.sanitizeColor(g)
        rb = self.sanitizeColor(b)

        self.ledStrip[y3 + 1] = self.gammaLookup[rr]
        self.ledStrip[y3]     = self.gammaLookup[rg]
        self.ledStrip[y3 + 2] = self.gammaLookup[rb]
        self.column[y3]   = rr
        self.column[y3+1] = rg
        self.column[y3+2] = rb




    def addLedColor( self, y, color ):
        y3 = y*3 
        rr = int(color[0])+self.column[y3+0]
        rg = int(color[1])+self.column[y3+1]
        rb = int(color[2])+self.column[y3+2]
        #logg( "set led color" + str(y) + ": (" + str(rr) + ", " + str(rg) + ", " + str(rb) )
        self.setLedRgb( y, rr,rg,rb )


    def scrollLeft( self ):
         for y in range( self.size-1 ):
            y3 = y*3
            self.setLedRgb( y, self.column[y3+3],self.column[y3+4],self.column[y3+5] )


class TempColumn:

    size        = SIZE
    column      = bytearray( SIZE * 3 + 1) # Whole strip in RGB 

    def __init__(self):
        logg( "Initializing TempColumn" )
        for i in range( SIZE ):
            self.setLedRgb( i, 0,0,0)

    def sanitizeColor( self, c ):
        sc = int(c)
        if ( sc > 254):
            sc = 254
        if ( sc < 0):
            sc = 0
        return sc

    def scrollRight( self ):
        for y in range( 1,self.size-1 ):
            ym = self.size-y
            y3 = ym*3
            self.setLedRgb( ym, self.column[y3-3],self.column[y3-2],self.column[y3-1] )


    def setLedRgb(self, y, r,g,b ):
        y3 = y * 3
        rr = self.sanitizeColor(r)
        rg = self.sanitizeColor(g)
        rb = self.sanitizeColor(b)

        self.column[y3]   = rr
        self.column[y3+1] = rg
        self.column[y3+2] = rb




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

    def initColor( self, ledStrip, color ):
        for i in range(ledStrip.getSize() ):
            ledStrip.setLedColor( i, color )



class LedShow:

    LedEffekts = None
    LedStrip = None
    stack = None

    def __init__(self):
        logg( "Initializing LedShow" )
        self.LedStrip = LedStrip()
        self.LedEffekts = LedEffekts()
        self.stack = []

    def stageLights( self ):
        for count in range( 1000 ):
            self.LedEffekts.initColor( self.LedStrip, (0,0,0) )
            self.LedEffekts.cloud( self.LedStrip, 30,sinLed( count *0.02, 70 ), (255,0,0) )
            self.LedEffekts.cloud( self.LedStrip, 40,sinLed( count *0.01, 70 ), (0,255,0) )
            self.LedEffekts.cloud( self.LedStrip, 40,sinLed( count *0.015, 70 ), (0,0,255) )
            self.LedStrip.show()
            time.sleep(0.01)


    def clear( self, type=0 ):
        co = TempColumn()
        mask = None
        delay = 0.01
        blocksize=1
        if type > 0:
            blocksize=5
        for count in range(SIZE/blocksize):
            if type > 0:
                for i in range(blocksize):
                    co.setLedRgb(1,255,255,255)
                    co.scrollRight()
                mask = co.column
                delay = 0.05
            if type < 1:
                self.LedStrip.scrollLeft()
            self.LedStrip.show( None, mask)
            time.sleep( delay )


    def colorChange( self ):
        for count in range( 1000 ):
            rr = sinLed(count*0.001, 127)
            rg = sinLed(count*0.0001, 127)
            rb = sinLed(count*0.01, 127)
            self.LedStrip.setLedRgb(155, rr,rg,rb )
            self.LedStrip.scrollLeft()
            self.LedStrip.show()
            time.sleep(0.001)

    def yellowScroll( self ):

        column2 = TempColumn()

        for count in range( 1000 ):
            rr = sinLed(count*0.01, 127)
            rg = 0
            rb = sinLed(count*0.005, 127)

            self.LedStrip.setLedRgb(155, rr,rg,rb )
            self.LedStrip.scrollLeft()

            rr = rg = rb = 0
            if (count % 160 < 24):
                rr=rg=int( 127+math.sin(count*0.003)*127 )
                rb=0

            column2.setLedRgb( 1, rr, rg,rb )
            if ( count%6  == 0 ):
                column2.scrollRight()
            summ = column2.column
            self.LedStrip.show( summ )
            time.sleep(0.01)


    def addToStack( self, method ):
        self.stack.append( method )

    def runStack( self):
        for me in self.stack:
            me()




def sinLed( count, width ):
    return int( width+math.sin( count )*width )



# how many LEDs do we have
width     = 32*5
column = bytearray(32*5 * 3 + 1)


# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."




column = Column( )
column.setInitMode( "clear" )
column.addEffect( ledEffekts.colorChange( 'left') )
column.addEffect( ledEffekts.scroll( 'right') )

column2 = StaticColumn( "fadeborders" )

ledShow = LedShow()
ledShow.addColumn( column )
ledShow.substractColumn( column2 )
ledShow.start(0.001)


count =0
print "Init done"
ledShow.addToStack( ledShow.colorChange  )
print "added1"
ledShow.addToStack( ledShow.clear(1) )
print "added2"

print "run now"

ledShow.runStack()
print "END now"

exit


while False:
    print count


    ledShow.colorChange()
    ledShow.clear(1)
    ledShow.stageLights()
    ledShow.clear()
    ledShow.yellowScroll()
    ledShow.clear()

    count=count+1
