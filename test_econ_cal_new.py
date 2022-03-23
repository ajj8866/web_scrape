import unittest
import os
from econ_cal_new import newsCalendar
import pandas as pd

class newsCalendar(unittest.TestCase):
    def setUp(self) -> None:
        self.calendar = newsCalendar()
    
    def tearDown(self) -> None:
        try:
            self.calendar.quitScrap()
        except:
            pass

    def testgetEvent(self):
        self.assertIsInstance(self.calendar.getEvent(), pd.DataFrame)


