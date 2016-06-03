# TradingCards

I work on this when I can, but I do have life events such as work and girlfriend problems!

## Goals
I have a few goals for this personal project.
* Create a Trading Card game! (Think collectible cards like Baseball or Football cards)
* Actually FINISH a python project and be satisfied with it.
* Look at forks from my friends over at /r/learnpython to see what they are up to and how I can learn from what they do
* Learn how to better use github revision control for my future career

## Files
These are the files and what they do

### Trading Card Game Structure.txt
This was just a quick idea I came up with at work while it was slow, but it gave me something to base my code on.

### TCGMain.py
This is the main file. This has all the classes (Card, Pack, Theme) and important code in it.

### TCGServer.py
Threaded TCP Server that handles incoming connections from clients. Also holds the functions to register\activate users.

### TCGTests.py
This holds the tests for testing that all the stuff works correctly

### TCGui.py
This is the testing GUI. As of now, it doesn't really work... :'( I'll get there one day.

### edit.py and create.py
Holds the functions that let you edit\create packs\themes

### regrules.py
Contains the rules for having a valid username\password\email for registration

## modules
Modules that I wrote to aid me.

#### pyemail.py
Gives me an easy lazy way to send simple emails to email addresses\phone numbers.

#### pyhash.py
My pure python implementation MD5, and a more condensed and clean pure python implementation of SHA384 (https://github.com/sfstpala/SlowSHA/blob/master/slowsha.py)

#### pyrand.py
My pure python implementation of some random generator functions.

#### pyqueue
My pure python implementation of Queues and DEQueues. Also contains pure python implementations of Singly linked lists and Doubly linked lists, the data structures used to make these.
