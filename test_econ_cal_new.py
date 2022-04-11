import unittest
import os
from econ_cal_new import newsCalendar
import pandas as pd

class newsCalendarTestCase(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Sets up two instances of newsCalendar class
        '''
        self.calendar = newsCalendar()
        self.calendar2 = newsCalendar()

    
    def tearDown(self) -> None:
        '''
        Closes and quits driver corresponding to class instances set on instantiation
        '''
        try:
            self.calendar.quitScrap()
            self.calendar2.quitScrap()
        except:
            pass

    def test_getEvent(self):
        '''
        Ensures data collected in format of dictionary and dataframe are of identical length
        '''
        #self.assertIsInstance(self.calendar.getEvent()[0], pd.DataFrame)
        x = self.calendar.getEvent()
        #y = self.calendar.getEvent()[1]
        print(x[0])
        self.assertEqual(len(x[0]), len(x[1]))

    def test_transformData(self):
        self.assertIsInstance(self.calendar2.transformData(), dict)


if __name__ == '__main__':
    unittest.main()