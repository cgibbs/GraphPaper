This is a graphing tool written in Python by Chance Gibbs. 
It is freely availabe under the GNU GPLv3. I really don't 
care what you do with/to it, but if you turn it into 
something nice, a little credit would be appreciated. I'm 
not doing a very professional job on this Readme because 
it's a simple little program, and I don't expect anyone to 
even notice it. Also, this is not a professional program, 
so I'm not going to dress it up like one. I wouldn't put 
on a suit and tie to give you a tour of my house, you know?

This module requires Pygame.

---- CONTROLS ----

COLOR SWITCHING

a: Black
e: Grey
w: White
r: Red
g: Green
b: Blue
o: Brown
d: Gold
y: Yellow

MODE SWITCHING

F1: Line
F2: Fill
F3: Fill Triangle
F4: Fill Circle
F5: Write Black
F6: Write White

LINE WIDTH

1: 1 pixel
2: 3 pixels
3: 5 pixels

OTHER

Escape: De-select node
Backspace: Clear screen
Backslash*: Re-draw grey points
Return: Re-draw lines

* The one above the Return key. I thought that one
was a forward slash, but Pygame disagrees. I mean, 
I thought the trick was to draw wheels under it, 
and the car faced the direction of the slash? Hmm. 
Anyway, it's the slash above the Return key, 
whichever one that is. 

---- HOW TO DO STUFF ----

It's pretty simple, really. In Line Mode, click somewhere, 
then click somewhere else. In Fill Circle Mode, you do the same,
and a circle is drawn centered on the first spot, with a radius 
out to the second spot. Fill Triangle Mode is the same way, 
but with a third click thrown in the mix, and it fills in the 
area inside the three points. Also, the places you can click 
include not just the grey points, but the middle points between 
them. Try it out, you'll see what I mean. In Fill Mode, you just 
click an area between the grey points, and it fills it in. In 
either write mode, you click a spot, then type a character, and 
it puts that character inside the grid square. Easy peasy.