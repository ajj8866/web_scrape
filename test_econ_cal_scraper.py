import unittest
#from Datapipe.econ_cal_new import newsCalendar
from econ_cal_scraper import EconCalScraper
import time
from econ_cal_new import newsCalendar
import os 
from pathlib import Path


class EconCalScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        '''
        Instantiates three instances of the EconCalScraper class:
        self.fin_cal: instantiated with tab set to financial calculator
        self.sentiment: Instantiated with tab set to economic sentiment
        self.heatmap: Instantiated with tab set to heatmap
        '''
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
        '''
        Ensures webpage URL opened on instantiaton of each insatnce is as expected
        '''
        self.assertEqual(self.fin_cal.driver.current_url, 'https://www.myfxbook.com/forex-calculators')
        self.assertEqual(self.sentiment.driver.current_url, 'https://www.myfxbook.com/community/outlook')
        self.assertEqual(self.heatmap.driver.current_url, 'https://www.myfxbook.com/forex-market/heat-map')

    def test_reset(self):
        '''
        Ensures class method reset changes URL tab to the one specified in the new_tb argument
        '''
        self.assertEqual(self.fin_cal.reset(new_tb='news').driver.current_url, 'https://www.myfxbook.com/streaming-forex-news')
    
    def test_mkFold(self):
        '''
        Ensures path exist on instantiation
        '''
        self.assertTrue(os.path.exists(Path(Path.cwd(), 'Datapipe','raw_data')))

    def test_getImgs(self):
        '''
        Ensures images scrapped are stored as dictionary 
        '''
        self.assertIsInstance(self.fin_cal.img_dict, dict)
        self.assertIsInstance(self.sentiment.img_dict, dict)
        self.assertIsInstance(self.heatmap.img_dict, dict)

        self.assertIsInstance(self.heatmap.img_list, list)

#    def test_getLinks(self):
#        pass

if __name__ == '__main__':
    unittest.main()
