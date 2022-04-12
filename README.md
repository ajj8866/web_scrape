# Web Scraper (Myfxbook and Crunchyroll)

## Note 
Initial website of choice was Crunchyroll given presence of capcha had to use another website for the purposes of scraping data. However, my alternative website (Myfxbook) didn't have a conventional cookies button so please refer to file scraper_class.py for milestones  and 2 while econ_cal_scraper.py, test_econ_cal_scraper.py and econ_cal_new.py for the remainder of the tasks. 

<u>econ_cal_scraper.py</u>: Provides methods for getting links, images, navigating across tabs and uploading image to s3 bucket and RDS, given primary data of choice is in tabular form and does not contain any images

<u>econ_cal_new.py</u>: Contains tabular data with ID column taken to unique identifier for any upcoming news announcement 


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
Site used is [myfxbook](https://www.myfxbook.com/), a financial news blog providing news, analysis and calendar updates on factors impacting forex markets 

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

| Method | Method Description |
| :-- | :-- |
| __init__ | In addition to data inherited from parent class instantiates an empty dataframe for storing variables in tabular form, a list of dictionaries with each dictionary storing a single observation variables and a dictionary of lists with each list containing all observations corresponding to a given column header. Both the list of dictionaries and dictionaries store identical differing only insofar as their convenience for different purposes; storing data in a dataframe and in a json file. For convenience also include option to connect to AWS RDS instance |
| getEvent | Uses beautifulsoup and selenium to scrape data in the news page storing such data in a dataframe and a list of dictionaries, appending a UUID and a formatted data variable, using datetime's strptime function for convenience in using pandas functions should the need arise.<br /> <br />Rescraping is prevented by using pandas drop_duplicates function. However, to allow for getting the latest update to the time remaining for a particular news event the last duplicate is retained. |
| transformData | Converts list of dictionaries, self.data, into dictionary of lists, self.data_dict |
| calData | Stores scraped data in json file, newws_data.json |
| toSql | Uploads dataframe self.df onto RDS instance |


## aws_scraper.py 
Includes a more comprehensive array of options with regards to interacting with AWS s3 or RDS instance

| Function | Function Description |
| :-- | :-- |
| aws_s3_upload | Uploads file 'upload_file' onto s3 bucker 'bucket_name' aliasing it as 'bucket_file_alias' |
| ls_buckets | List all buckets existing in s3 instance |
| aws_s3_upload_folder | Uploads all file existing in folder specified in 'argument' onto bucket 'bucket_name'. By default 'path' points to image folder in current working directory which stores images |

## test_econ_cal_scraper.py 
Unit test file for econ_cal_scraper.py. 

| Method | Description |
| :-- | :-- |
| setUp | Instantiates three instances of EconCalScraper class each navigating to a different tab |
| tearDown | Ensure each instance started up on setUp method |
| test_getImgs | Checks whether the img_dict attribute is of type dict when calling getImgs |
| test_mkFold | Checks the image folder |
| test_getPage | Ensures each class instance is navigated to the current URL on instantiation |
| test_reset | Ensure tab is succesfully set to the one specified in new_tb argument |


## test_econ_cal_new.py
| Method | Description |
| :-- | :-- |
| setUp | Instantiates two instances of newsCalendar class |
| tearDown | Ensure each instance started up on setUp method |
| test_getEvent | Calls and tests the getEvent method which yield a tuple of a list of dictionaries and a dataframe, each containing the same data. The test checks both are of the same length |
| test_tranformData | Ensures on calling the transformData method the list of dictionaries is transformed to a dicionary of list |

## Screenshots for Milestones 
<img width="968" alt="image" src="https://user-images.githubusercontent.com/100163231/163034690-6924e046-6ac6-425e-8958-1c27bab23959.png">





