import os.path


def get_resource_path(relpath):
	"""
	Returns the absolute filepath to a resource. The relpath is the
	relative path of it wrt to the res directory. If the resource is
	for example res/img/cards/2h.png the relpath should be
	"img/cards/2h.png".
	"""
	# find absolute path of res directory:
	resourcepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "res"))
	# join it with the relative path:
	return os.path.join(resourcepath, relpath)
