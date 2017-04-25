MVC
===

This describes the implementation of the model view control pattern (MVC)
I used for the development of Shithead.

## Information transfer

To transfer information between the model and the view via the controller I use two different "mechanisms":

* Requests
* CardStrings

## Request

The following requests, which inherit from a `Request` superclass, are available in Shithead:

* `RequestQuit`
* `RequestInitialBoard`
* `RequestPlay`
* `RequestTake`

## CardString

The model sends lists of CardStrings to the controller. A CardString is a regular string that represents a single playing card. It uses the default two letter notation that you might be familiar with, e.g. 

* "4h" for the four of hearts
* "tc" for the ten of clubs
* "qd" for the queen of diamonds. 

No "sensitive" information should be sent from the model to the view, therefore hidden cards are displayed as "??". Empty card places in a `CardRow` are represented by "xx".

