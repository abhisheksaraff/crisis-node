
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from verification.utils.Whereisfire import firesin
from verification.utils.whereisflood import floodsin

import unittest

class TestStringMethods(unittest.TestCase):

    def testfi_answer(self):
        floridawildfire=firesin((-84.73,  29.965, -84.07, 30.3))
        assert floridawildfire >= 1
        assert floridawildfire<=2
    def testfi_on(self):
        loweronwildfire=firesin((-83,42,-74,46))#
        assert loweronwildfire <= 1
    def testfi_ssu(self):
        ssufire=firesin((23.8869795809, 3.50917, 35.2980071182, 12.2480077571))
        assert ssufire >= 1

    def testfi_aus(self):
        ausfire=firesin((152, -32.8, 152.6, -31.4))
        assert ausfire >= 1

    def testw_moz1(self):
        assert floodsin(-25.075,33.575)[1]=="This is really quite bad. " #an area of the limpopo which recently flooded


    def testw_moz2(self):
        assert floodsin(-24.93,33.62)[1]=="This is really quite bad. "
    def testw_stl(self):
        assert floodsin(46.33, -72.52)[1]=="probably not major flooding"

    def testw_ytz(self):
        assert floodsin(31.78, 120.985)[1]=="probably not major flooding"

    def testw_ytz(self):
        assert floodsin(31.78, 120.985)[1]=="probably not major flooding"
    def test2_com(self):
        assert floodsin(49.7,-125)[1]=="This is a flood"

if __name__ == '__main__':
    unittest.main()