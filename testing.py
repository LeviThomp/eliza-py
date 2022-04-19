import unittest
from utils import arrays


class TestEliza(unittest.TestCase):

    def testcase():
        return(200)

    # Testing that external files can change the name
    def testNameChange(self):
        self.assertEqual("Eliza", arrays.displayNameSetting)
        arrays.displayNameSetting = "BillyBob"
        self.assertEqual("BillyBob", arrays.displayNameSetting)




