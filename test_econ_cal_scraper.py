import unittest
#from Datapipe.econ_cal_new import newsCalendar
from econ_cal_scraper import EconCalScraper
import time
from econ_cal_new import newsCalendar
import os 
from pathlib import Path


class EconCalScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.fin_cal = EconCalScraper(tab='fin_cal')
        self.sentiment = EconCalScraper(tab='sentiment')
        self.heatmap = EconCalScraper(tab='heatmap')
    
    def tearDown(self) -> None:
        try:
            self.fin_cal.quitScrap()
            self.sentiment.quitScrap()
            self.heatmap.quitScrap()
        except Exception as e:
            print(e)
            pass

    def test_getPage(self):
        self.assertEqual(self.fin_cal.driver.current_url, 'https://www.myfxbook.com/forex-calculators')
        self.assertEqual(self.sentiment.driver.current_url, 'https://www.myfxbook.com/community/outlook')
        self.assertEqual(self.heatmap.driver.current_url, 'https://www.myfxbook.com/forex-market/heat-map')

    def test_reset(self):
        self.assertEqual(self.fin_cal.reset(new_tb='news').driver.current_url, 'https://www.myfxbook.com/streaming-forex-news')
    
    def test_mkFold(self):
        self.assertTrue(os.path.exists(Path(Path.cwd(), 'Datapipe','raw_data')))

    def test_getImgs(self):
        self.assertIsInstance(self.fin_cal.img_dict, dict)
        self.assertIsInstance(self.sentiment.img_dict, dict)
        self.assertIsInstance(self.heatmap.img_dict, dict)

#    def test_getLinks(self):
#        pass

if __name__ == '__main__':
    unittest.main()
