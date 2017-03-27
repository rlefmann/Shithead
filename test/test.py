# This is a generic testcase. In the end every file in the program's
# source directory should have a testcase in a separate file inside
# this directory.

import unittest

class Testcase(unittest.TestCase):
	
	def test_function_1(self):
		pass
		
		
if __name__ == "__main__":
	unittest.main(exit=False)
