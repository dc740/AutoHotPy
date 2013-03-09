AutoHotPy
=========

It started as an AutoHotKey replacement using Incerception driver, but now its a fully working automation tool. You can record activities to repeat them, or you can manually program them.

#FAQ

##Why? just... why?
AutoHotKey is great, but many games and programs don't work with it. And the ones that work have many counter-measures to stop it (because many script kiddies use it to cheat!).
I'm against cheating in games, but I'm also against discrimination. Many players have different kinds of disabilities, and they need helping tools to play.
I believe everyone deserves the right to choose which game, or program they want to use without limitations.

##How is it different?
AutoHotPy is a scripting tool, just like AutoHotKey, but it uses Interception library (https://github.com/oblitum/Interception).
The great thing is that Interception uses a very low level driver to capture keyboard and mouse events, which makes it perfect for games that have problems with AutoHotKey

##Why python?
Because when you write AutoHotPy scripts, you learn a real programming language that you can later use to write your own programs.

##Installation
AutoHotPy doesn't really need any. You just place the scripts in the same folder and they just work. However, the libraries needed for it to run are not installed by default in any operative system.

1.    Verify you have Python installed, if not, please install python to proceed
2.    Install interception driver (and restart your computer): http://oblita.com/Interception.html
hint: if double clicking in the executable doesn't install the driver (you will see an error message when you start AutoHotPy), try running a command line as administrator from the windows menu (right clicking on the program and selecting "Run as administrator"), and then go to your download location from the command line and run "install-interception.exe /install"
3.    Place the .dll in the same place were you downloaded AutoHotPy. We need interception.dll to work!


##Intro
Python is a real programming language, so remember: everything you learn while you write the scripts can be used to write your own programs!
To use AutoHotPy you only have to write a script (patience!) and place it in the same folder where you installed the app.
I will add more documentation later but lets get you working fast.


Open "Example1-GameCombo.py". The first paragraph is the license, you don't need it in your scripts.
Follow the comments (everything that is placed after #) to understand what's happening.


"Example2-MultipleKeys.py": this example shows how to handle multiple keys pressed at the same time. 
The example opens the windows task manager (in windows 7) directly when you hit Ctr+Alt+Supr instead of taking you
to the options screen.
The trick is to remap Ctrl+Alt+Supr to Ctrl+Shift+Escape (that opens the task manager directly)
There is literally no limit on how many pressed keys you can handle from AutoHotPy, but that doesn't mean the operative system won't have his own limitations.


"Example3-MouseButtons.py": Handling mouse movement and clicks is the hardest part in AutoHotPy, but because you have to do each movement or click manually.

"Example4-MouseMovement.py": Invert mouse axis

"Example5-Macros.py": Shows how to record macros for keyboard and mouse

"Example6-Macros2 - Gaming macros.py": Shows how to record macros for games, where the mouse starting position is important for the macro to success.

"Example7-Macros3 - Saving macro to file.py": the title is quite descriptive.

IMPORTANT NOTE:
Known bug: the script crashes after saving a macro to file and then trying to run the macro again. Workaround: restart the application after saving a macro to a file.

##Running the scripts
To run any of the scripts open a command line and run "python <yourscript>.py". That's all you need.

Be patient! Don't panic if you need help with the language, there are many python developers around the world.
You will find help in any language you can image.



Copyright 2012 Emilio Moretti <emilio.morettiATgmailDOTcom>
This program is distributed under the terms of the GNU Lesser General Public License.
