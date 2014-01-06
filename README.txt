---- INTRO ----

This is a graphing tool written in Python by Chance Gibbs. It 
is freely available under the GNU GPLv3. I really don't care 
what you do with/to it, but if you turn it into something nice, 
a little credit would be appreciated. I'm not doing a very 
professional job on this Readme because it's a simple little 
program, and I don't expect anyone to even notice it. Also, 
this is not a professional program, so I'm not going to dress 
it up like one. I wouldn't put on a suit and tie to give you a 
tour of my house, you know?

---- USAGE ----

NOTE: gpOriginal is only there to remind me how terrible my 
original program was. I don't really recommend using it at all,
because the other two versions are much better.

You can run either gpOriginal.py, gpRefactor.py, or gpObjOr.py.
gpOriginal and gpRefactor operate more or less the same, though
gpRefactor has more features, and is more updated in general.
gpObjOr is the newest version, and it behaves differently.
Basically, gpObjOr uses one unified object list, so that the
most recent additions are drawn on top, rather than 
letters>lines>fill>etc. Both have their advantages and 
disadvantages, so I thought I'd leave them both in, so that the
two people in the world that ever use this don't get into a 
heated argument.

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
F5: Write
F6: Symbol

LINE WIDTH

1: 1 pixel
2: 3 pixels
3: 5 pixels

OTHER

Escape: Exit current drawing mode
Backspace: Remove last drawn object (in mode, if using gpRefactor)
Delete: Clear Screen
Home: Save
End: Load

---- HOW TO DO STUFF ----

It's pretty simple, really. In Line Mode, click somewhere, 
then click somewhere else. Fill Triangle Mode is the same 
way, but with a third click thrown in the mix, and it fills 
in the area inside the three points. Circle Mode is like 
Line Mode, but it draws a filled circle centered at the first
click, with a radius out to the second click. In Write Mode and
symbol mode, you click to pick a square, and type a letter, and 
it prints the letter in the square. In Fill Mode, you just click 
an area between the grey points, and it fills it in. Easy peasy. 
Also, the places you can click include not just the grey points, 
but the halfway points between them. Try it out, you'll see what 
I mean.