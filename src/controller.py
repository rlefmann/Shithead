# The Controller is the center piece of the program. It creates an
# instance of the game model and the view (mainwindow). The computer
# player (ai) is initialized here, too.

class Controller:
	
	def __init__(self):
		# create instance of model, view and ai
		pass
		
	def on_event(self,event):
		# here all the message handling is performed. The method
		# determines what type of event was given to it and then
		# performs the appropriate actions.
		pass



########################################################################
# Events are what is send by the controller between the model and the
# view and are the basic messages of the mvc pattern
########################################################################


class Event:
	"""A generic event that is the base class of all other events."""
	def __init__(self):
		self.name = "generic event"


class QuitEvent(Event)
	"""
	The program should end after creating this event.

	It is created, when the pygame window is closed or when the escape
	button is pressed.
	"""
	def __init__(self):
		self.name = "Quit event"


