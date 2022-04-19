import unittest
from utils import arrays


class TestEliza(unittest.TestCase):

    def testcase():
        return(200)

    # Testing that external files can change the name
    def testNameChange(self):
        self.assertEquals("Eliza", arrays.displayNameSetting)
        arrays.displayNameSetting = "BillyBob"
        self.assertEquals("BillyBob", arrays.displayNameSetting)



