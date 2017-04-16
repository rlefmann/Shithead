from model.settings import Settings
from model.game import *

class Controller:
	"""
	The Controller is the center piece of the program. It creates an
	instance of the game model and the view (mainwindow). The computer
	player (ai) is initialized here, too.
	"""
	def __init__(self):
		"""
		Sets up a new controller and creates model and view.

		A Game object is created, as well as a view object. The class
		method `on_view_event` is added as listener and the main loop
		of the PyGame window is started by calling `run`.
		"""
		# Create a settings object with default values
		# TODO: allow to change these values?
		settings = Settings()
		# the model:
		self.game = Game(settings)
		# create the ai that simulates the opponent player:
		# TODO: maybe other ai's should be allowed, too
		self.ai = StraightforwardAI(self.game)
		
		
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


