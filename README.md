# Web Scraper (Myfxbook and Crunchyroll)

## Note 
Initial website of choice was Crunchyroll given presence of capcha had to use another website for the purposes of scraping data. However, my alternative website (Myfxbook) didn't have a conventional cookies button so please refer to file scraper_class.py for milestones  and 2 while econ_cal_scraper.py, test_econ_cal_scraper.py and econ_cal_new.py for the remainder of the tasks 

## Crunchyroll Webscraper
Site used is [crunchyroll](https://www.crunchyroll.com/en-gb), a streaming service for watching anime.


| Method | Method Description |
| :-- | :-- |
| accRejCookies | Reject non-essential cookies if rej set to false otherwise accepts non-essential cookies |
| getShows | Navigates to tab showing anime |
| pickSection | Sorts by one of popularity, most recen or alphabetically depending on argument chose |
| getAlphaPg | Lists shows beginngin with a given letter |
| filterGenre | Filters shows listed by genre |

## Myfxbook 
Financial news blog providing news, analysis and calendar updates on factors impacting forex markets 

#### <u>econ_cal_scraper.py</u> 

| Method | Method Description |
| :-- | :-- |
| __init__ | Navigates to tab chosen in the tab argument, instantiates chrome driver, an empty list of dictionaries for storing links and image IDs which may be scrapped using the scrapper |
| getPage | Used on instantiation and navigates to tab chosen by user using the tab argument |
| popupEsc | Refreshed driver in the event a popup advertisment shows up, waiting a maximum of 15secs for the advertisement to show up before moving on using selenium's WebDriverWait method |
| getImgs | Yields all iimages on relevant page storing such images into self.img_dict |
| addUUID | Convenience method primarily used in other methods to set UUID using uuid library |
| mkPath | Makes folder raw_data should it not alredy exist |
| mkImgFold | Makes images subfolder within raw_data |
| uploadImg | Uploads images scrapped and stored in img_dict onto images subfolder within raw_data |
| archImg | Creates (if it does not already exist) a json file which shall store json object |
| allLinks | Class method navigating to all possible tabs on Myfxbook homepage, collecting all links existing on each tab and appending them to a list. Finally set operation is applied on the list to yield all unique links  |

#### <u>econ_cal_new.py</u> 
Class inheriting from econ_cal_scraper. Navigates specifically to economic calendar tab and getEvent tab is subsequently used to encapsulate the each piece of economic news into a dataframe containing columns ID (using uuid4), Date, Formatted date (to allow for filtering), Time to Event, Country, Event, Impact (high, medium or low), Consensus (analyst estimate of any figure), Actual (actual value of any financial figure) 
