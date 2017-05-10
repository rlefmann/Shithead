from setuptools import setup, find_packages

setup(
	name="shithead",
	version="0.1",
	description="The card game Shithead implemented in Python and PyGame.",
	url="https://bitbucket.org/Prxxxe/shithead",
	author="Raoul Lefmann",
	author_email="raoul.lefmann@gmail.com",
	license="GNU GPL",
	packages=find_packages(),
	package_data={
		"shithead": ["res/*"]
	},
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"shithead=shithead.__main__:main",
		]
	},
	install_requires = ["pygame"],
	zip_safe = False,
	#data_files=[
	#	("img/cards/", glob.glob("img/cards/*.png"))
	#]
)
