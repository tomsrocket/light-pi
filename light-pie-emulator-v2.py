#!/usr/bin/python

import sys

# logging 
def logg( msg):
    print msg;

devMode = 0

logg( "arguments " + str(len(sys.argv)) )
if ( len(sys.argv) > 1 ):
    if ( sys.argv[1] == "dev" ):
        devMode = 1

import math
import random
import time

spidev = None

if ( devMode == 0 ):
    import RPi.GPIO as GPIO, Image, time
    dev       = "/dev/spidev0.0"
    spidev    = file(dev, "wb")
else:
    import pygame

#import LedLib 


class LedEffekts: 

    def cloud( self, column, size, pos, color ):  # size = pos => 0-100(%)
        stripSize = column.size;
        pixel = 1;
        mid = pos*pixel
        start = pos*pixel - size*pixel
        if ( start < 0 ):
            start = 0
        end =  pos*pixel + size*pixel
        if ( end > stripSize ) :
            end = stripSize
        step = math.pi/ ( (end-start)  if (end-start) > 0.0001 else 0.0001 )
        for i in range(start,end):
            colo = self.decreaseColor( color,  math.sin( (i-start)*step) )
            column.addLedRgb( i, colo[0], colo[1], colo[2] )


    def decreaseColor( self, color, percentage ):
        if ( percentage > 1 ):
            percentage = percentage / 100
        pc =  percentage
        color  = ( color[0]*pc, color[1]*pc, color[2]*pc )
        return color

    def initColor( self, ledStrip, color ):
        for i in range(ledStrip.getSize() ):
            ledStrip.setLedColor( i, color )





SIZE = 32*5
EFFECTS = LedEffekts()


#
# LedStrip
# Singleton class to control the LED strip
#
class LedStrip:
    size = SIZE
    column      = bytearray( size * 3 + 1) # Whole strip in gamma corrected data, ready to be sent to spidev.
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
        if ( devMode > 0 ):
            pygame.init() 
            self.screen = pygame.display.set_mode((640+161*2, 100)) 


    def sanitizeColor( self, c ):
        sc = int(c)
        if ( sc > 255):
            sc = 255
        if ( sc < 0):
            sc = 0
        return sc

    def show( self ):
        leds = self.ledStrip
        cols = self.column
        show = self.column

        for y in range(self.size):
            y3=y*3
            rr = self.sanitizeColor(cols[y3+0] )
            rg = self.sanitizeColor(cols[y3+1] )
            rb = self.sanitizeColor(cols[y3+2] )
            if ( devMode > 0 ):
                pygame.draw.rect(self.screen,(rr,rg,rb),[y*6,20,5,5])

            leds[y3 + 1] = self.gammaLookup[int(rr)]
            leds[y3]     = self.gammaLookup[int(rg)]
            leds[y3 + 2] = self.gammaLookup[int(rb)]
        
        if ( devMode == 0 ):
            spidev.write(leds)
            spidev.flush()
        else:
            pygame.display.flip()

        self.clear()

    def clear( self ):
        self.column = map( lambda x: 0, self.column )

    def getColumn( self ):
        return self.column


    def addColumn( self, add, sub ):
        #print "LedStrip "+str(id(self))+" adding ("+str(sub)+") effect " + str(id(add) ) 

        if ( sub < 0):
            cols = map(lambda x, y : x - y, self.column, add)
        else:
            cols = map(lambda x, y : x + y, self.column, add)
        self.column = cols


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









class StaticColumn: 

    size = SIZE
    effects = []
    column      = bytearray( SIZE* 3 + 1)

    def __init__(self):
        logg( "Initializing StaticColumn" )
        self.column      = bytearray( self.size* 3 + 1)
        self.effects     = []


    def getColorAt( self, y ):
        y3 = y*3;
        if ( y3 < 0): 
            return (0,0,0)
        if ( y3 > ((self.size-1)*3) ):
            return (0,0,0)
        return ( self.column[y3+0], self.column[y3+1], self.column[y3+2] )

    def sanitizeColor( self, c ):
        sc = int(c)
        if ( sc > 255):
            sc = 255
        if ( sc < 0):
            sc = 0
        return sc

    def clear( self ): 
        self.column = map( lambda x: 0, self.column )


    def _getY3( self, y):
        if ( y < 0): 
            y = 0
        if ( y > self.size-1 ):
            y = self.size-1
        return y*3

    def setLedRgb(self, y, r,g,b ):
        y3 = self._getY3(y)
        rr = self.sanitizeColor(r)
        rg = self.sanitizeColor(g)
        rb = self.sanitizeColor(b)

        self.column[y3]   = rr
        self.column[y3+1] = rg
        self.column[y3+2] = rb

    def addLedRgb( self, y, r,g,b ):
        y3 = y*3 
        rr = int(r)+self.column[y3+0]
        rg = int(g)+self.column[y3+1]
        rb = int(b)+self.column[y3+2]
        self.setLedRgb( y, rr,rg,rb )

    def getColumn( self, counter ):
        return self.column

    def addEffect( self, effect ):
        print "StaticColumn "+str(id(self))+" adding effect " + str(id(effect) ) 
        effect.applyToColumn( self, 0 )

    def setColumn( self, col ):
        self.column = col



class Column(StaticColumn):

    def __init__(self):
        logg( "Initializing Column "+ str(id(self) ) )
        self.column      = bytearray( self.size* 3 + 1)
        self.effects     = []

    def addEffect( self, effect ):
        print "Column "+str(id(self))+" adding effect " + str(id(effect) ) 
        self.effects.append( effect )


    #
    # apply all effects and return this column LED ARRAY
    #
    def getColumn( self, counter ):
        for effect in self.effects:
            effect.applyToColumn( self, counter )
        return self.column



class LedShow:

    columns = []
    ls = LedStrip()
    lastCol = bytearray( SIZE* 3 + 1)


    def addColumn( self, column ):
        self.columns.append( ( column, 1 ) )

    def subColumn( self, column ):
        self.columns.append( ( column, -1 ) )

    def show( self, timer, rangeStart, rangeEnd ):
        rangeEnd = rangeEnd * 3;
        ls = self.ls
        for col in self.columns:
            print "has column " + str(id(col[0]))
            for eff in col[0].effects:
                print "has effect " + str(id(eff))

        for counter in range( rangeStart,rangeEnd ):
            for column in self.columns: 
                c = column[0].getColumn( counter )
                ls.addColumn( c, column[1] ) 
            ls.show()

            time.sleep( timer )

        for column in self.columns: 
            c = column[0].getColumn( counter )
            ls.addColumn( c, column[1] ) 

        time.sleep( timer )

        self.lastCol = ls.getColumn()
        ls.clear()

    def deleteColumns( self ):
        self.columns=[]

    def clear( self, type=0 ):
        self.columns=[]

        column = Column( )
        column.setColumn( self.lastCol )
        column.addEffect( Fadeout( 0.05 ) )
        column.addEffect( Scroll( 'right') )
        self.addColumn( column )
        self.show(0.02, 0, 50 )
        self.columns=[]






def sinewave( count, width ):
    return int( width+math.sin( count )*width )





#
# effects
#

class BaseEffect: 
    size = SIZE
    def perform( self, counter ):
        print "BaseEffect is performing"

class SolidDot( BaseEffect ):
    pos    = 0    
    col    = (0,0,0)
    def __init__( self, pos, col):
        self.pos = pos
        self.col= col

    def applyToColumn( self, column, counter ):
        column.setLedRgb( self.pos, self.col[0], self.col[1], self.col[2])


class ColorDot( BaseEffect ):
    pos    = 0
    speed  = 0.01    
    def __init__( self, pos, speed = 0.01):
        self.pos = pos
        self.speed=speed

    def applyToColumn( self, column, counter ):
        where = self.pos
        column.setLedRgb( where, sinewave( counter*self.speed, 127 ), sinewave( counter*2*self.speed, 127 ), sinewave( counter*3*self.speed, 127 ))


class Fadeout( BaseEffect ):
    amount    = 0.9    
    def __init__( self, a ):
        self.amount = 1-a

    def applyToColumn( self, column, counter) :
        for y in range( column.size ):
            col = column.getColorAt( y )
            column.setLedRgb( y, col[0]*self.amount, col[1]*self.amount, col[2]*self.amount )

class ClearColumn( BaseEffect ):
    def applyToColumn( self, column, counter ):
        column.clear()


class Scroll( BaseEffect ):
    direction = "right"
    def __init__( self, direction ):
        self.direction = direction

    def applyToColumn( self, column, counter ):
        if ( self.direction == "left"):
             for y in range( column.size ):
                col = column.getColorAt( y+1 )
                column.setLedRgb( y, col[0], col[1], col[2] )
        else: 
             for y in range( column.size ):
                my = column.size-1 - y
                col = column.getColorAt( my )
                column.setLedRgb( my+1, col[0], col[1], col[2] )



class SolidCloud( BaseEffect ):
    def __init__( self, size, pos, color ):
        self.width = size
        self.pos = pos
        self.color=color
    def applyToColumn( self, column, counter ):
        EFFECTS.cloud(column, self.width, self.pos, self.color )





class StageLights( BaseEffect ):
    def __init__( self ):
        self.width = random.randint(10, 80)
        self.speed = ( random.uniform(0.0005, 0.02), random.uniform(0.0005, 0.02), random.uniform(0.0005, 0.02) )
        self.color = ( random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1) )
        logg( self.speed )
    def applyToColumn( self, column, counter ):
        EFFECTS.cloud( column, self.width,sinewave( 0.0 + counter * self.speed[0], 70 ), (255*self.color[0],0,0) )
        EFFECTS.cloud( column, self.width,sinewave( 0.0 + counter * self.speed[1], 70 ), (0,255*self.color[1],0) )
        EFFECTS.cloud( column, self.width,sinewave( 0.0 + counter * self.speed[2], 70 ), (0,0,255*self.color[2]) )


class BlockFadeOut( BaseEffect ):

    def TODO(self):
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


class Blink( BaseEffect ):
    def __init__( self, pos, color, width1, width2, offset=0 ):
        self.w1 = width1
        self.w2 = width2
        self.col = color
        self.pos = pos
        self.offset = offset
    def applyToColumn( self, column, counter ):
        if ( (counter+self.offset) % (self.w1+self.w2) < self.w2):
            rr=self.col[0]
            rg=self.col[1]
            rb=self.col[2]
            column.addLedRgb( self.pos, rr, rg,rb )








ledShow = LedShow()
# ====================================================>
while True:

    for i in range(1,10):

        # Random color dot worm
        column = Column( )
        column.setColumn( ledShow.lastCol )
        ledShow.deleteColumns()
        column.addEffect( SolidDot( 0, (0,0,0) ) )
        wormoSize = random.randint(2, 20)
        column.addEffect( Blink( 0, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), wormoSize, wormoSize, 0 ) )
        column.addEffect( Blink( 0, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), wormoSize, wormoSize, wormoSize ) )
        column.addEffect( Scroll( 'right') )
        ledShow.addColumn( column )
        cSpeed = random.uniform(0.03, 0.05)
        ledShow.show(cSpeed, 0, random.randint(20, 80) )

        column = Column( )
        column.setColumn( ledShow.lastCol )
        ledShow.deleteColumns()
        column.addEffect( SolidDot( 0, (0,0,0) ) )
        column.addEffect( Scroll( 'right') )
        ledShow.addColumn( column )
        ledShow.show( cSpeed, 0, 1 )

    ledShow.clear()
    # ====================================================>

    # Stage lights
    column = Column( )
    column.addEffect( ClearColumn() )
    column.addEffect( StageLights( ) )
    ledShow.addColumn( column )

    ledShow.show(0.01, 0, 600 )
    ledShow.clear()
    # ====================================================>

    # Three holes
    column = Column( )
    column.addEffect( ColorDot( 0,0.01 ) )
    column.addEffect( Scroll( 'right') )
    ledShow.addColumn( column )

    holeSize = random.randint(5, 20)
    holeDepth = random.uniform(0.03, 1)
    column = StaticColumn()
    column.addEffect( SolidCloud( holeSize,SIZE/2,(255*holeDepth,255*holeDepth,255*holeDepth) ) )
    holeDepth = random.uniform(0.03, 1)
    column.addEffect( SolidCloud( holeSize,SIZE*3/4,(255*holeDepth,255*holeDepth,255*holeDepth) ) )
    holeDepth = random.uniform(0.03, 1)
    column.addEffect( SolidCloud( holeSize,SIZE*1/4,(255*holeDepth,255*holeDepth,255*holeDepth) ) )
    ledShow.subColumn( column )

    ledShow.show(0.01, 0, 600 )
    ledShow.clear()
    # ====================================================>

    # Christmas dots
    column = Column( )
    distance = random.randint(10, 100)
    width = random.randint(1, 5)
    column.addEffect( SolidDot( 0, (0,0,0) ) )
    column.addEffect( Blink( 0, (255,0,0), distance, width, 0 ) )
    column.addEffect( Blink( 0, (255,255,255), distance, width, distance/2+width/2 ) )
    column.addEffect( Scroll( 'right') )
    ledShow.addColumn( column )

    ledShow.show(random.uniform(0.02, 0.05), 0, 400 )
    ledShow.clear()
    # ====================================================>

    # Quick color scrolls
    column = Column( )
    colorSpeed = random.uniform(0.01, 0.1)
    column.addEffect( ColorDot( 0,colorSpeed) )
    column.addEffect( Scroll( 'right') )
    column.addEffect( Fadeout( random.uniform(0.01, 0.05) ) )
    ledShow.addColumn( column )

    column = Column( )
    column.addEffect( ColorDot( SIZE, colorSpeed) )
    column.addEffect( Scroll( 'left') )
    column.addEffect( Fadeout( random.uniform(0.01, 0.05) ) )
    ledShow.addColumn( column )

    ledShow.show(0.02, 0, 400 )
    ledShow.clear()
    # ====================================================>

    # window sizes
    #12 +32
    #42
    #32
    #42







print "END now"
