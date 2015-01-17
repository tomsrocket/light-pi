
//
// This is for my Badezimmerspiegel Arduino Mega (ATmega1280)
//


// Use if you want to force the software SPI subsystem to be used for some reason (generally, you don't)
// #define FORCE_SOFTWARE_SPI
// Use if you want to force non-accelerated pin access (hint: you really don't, it breaks lots of things)
// #define FORCE_SOFTWARE_SPI
// #define FORCE_SOFTWARE_PINS
#include "FastLED.h"

///////////////////////////////////////////////////////////////////////////////////////////
//
// Move a white dot along the strip of leds.  This program simply shows how to configure the leds,
// and then how to turn a single pixel white and then off, moving down the line of pixels.
// 

// How many leds are in the strip?
#define NUM_LEDS 48

// Data pin that led data will be written out over
#define DATA_PIN 2

// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define CLOCK_PIN 3

// This is an array of leds.  One item for each led in your strip.
CRGB leds[NUM_LEDS];

// This function sets up the ledsand tells the controller about them
void setup() {
	// sanity check delay - allows reprogramming if accidently blowing power w/leds
   	delay(500);

      // Uncomment one of the following lines for your leds arrangement.
      // FastLED.addLeds<TM1803, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<TM1804, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<TM1809, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<WS2812, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
      // FastLED.addLeds<WS2811_400, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<GW6205, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<GW6205_400, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<UCS1903, DATA_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<UCS1903B, DATA_PIN, RGB>(leds, NUM_LEDS);

      // FastLED.addLeds<WS2801, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<SM16716, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<LPD8806, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<P9813, RGB>(leds, NUM_LEDS);
      
      //FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
      // FastLED.addLeds<SM16716, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
      FastLED.addLeds<LPD8806, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
}

// This function runs over and over, and is where you do the magic to light
// your leds.
double currentColor = ((double) rand() / (RAND_MAX)) * 255;
double i = 0;
void loop() {



  
 
//  for ( double i = 0 ; i < 255 ; i = i  + 0.1 ) {

     double brightness = sin(i) * 20 + 100;
     i = i + 0.1;
     
     
     currentColor = currentColor +0.3 ;
     if ( currentColor > 255 )  { currentColor = 0; }
     
     int myCol = currentColor ;
     for(int whiteLed = 0; whiteLed < NUM_LEDS; whiteLed = whiteLed + 1) {
        myCol = myCol +2;
        if ( myCol > 255 ) {
          myCol=0;
        }
       
        leds[whiteLed] = CHSV( myCol, 255, brightness );
      }

     // Show the leds (only one of which is set to white, from above)
     FastLED.show();

      // Wait a little bit
     delay(30);

//  }

}
