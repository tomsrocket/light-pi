


ARDUiNO IDE
===========

How to add a library to Arduino IDE:

Select "Sketch -> Import Library -> Add Library .."
Then Go into the directory where your library is a subdirectory. 
(eg go in the the directory where the subdirectory "FastLED_303" resides. Do NOT go into the directory FastLED_303!))
Single click the library subdirectory (eg. FastLED_303) (so that it is highlighted)
THEN click OK.  

=> This is the only way that works. Arduino IDE is very buggy!





FLORA INSTRUCTIONS
==================

Please note:

- You need to use an extra compiled arduino IDE for use with the Adafruit FLORA. Download it at adafruit.
- In the arduino IDE in the menu Tools->Programmer use "AVRISP mkII" 

- If it doesn't work (error message says something about Leonardo not being found) then always do this: 
 - after you click upload, and then after "compile" disappears and "upload" is displayed wait 1sec and press the reset button on the Flora (Works for me perfectly every time on windows)



