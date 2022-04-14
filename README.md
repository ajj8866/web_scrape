# Web Scraper (Myfxbook and Crunchyroll)

## Note 
Initial website of choice was Crunchyroll given presence of capcha had to use another website for the purposes of scraping data. However, my alternative website (Myfxbook) didn't have a conventional cookies button so please refer to file scraper_class.py for milestones 1 and 2 while econ_cal_scraper.py, test_econ_cal_scraper.py and econ_cal_new.py for the remainder of the tasks. 

<u>econ_cal_scraper.py</u>: Provides methods for getting links, images, navigating across tabs and uploading image to s3 bucket and RDS, given primary data of choice is in tabular form and does not contain any images

<u>econ_cal_new.py</u>: Contains tabular data with ID column taken to unique identifier for any upcoming news announcement 


## Crunchyroll Webscraper
Site used is [crunchyroll](https://www.crunchyroll.com/en-gb), a streaming service for watching anime.

Please use the following options for headless_op depending on whether running locally or on EC2:
- True: If running on EC2
- False: If running on local machine

| Method | Method Description |
| :-- | :-- |
| accRejCookies | Reject non-essential cookies if rej set to false otherwise accepts non-essential cookies |
| getShows | Navigates to tab showing anime |
| pickSection | Sorts by one of popularity, most recen or alphabetically depending on argument chose |
| getAlphaPg | Lists shows beginngin with a given letter |
| filterGenre | Filters shows listed by genre |

## Myfxbook 
Site used is [myfxbook](https://www.myfxbook.com/), a financial news blog providing news, analysis and calendar updates on factors impacting forex markets 

### <u>econ_cal_scraper.py</u> 

<u>Class Name: EconCalScraper</u>

| Method | Method Description |
| :-- | :-- |
| __init__ | Navigates to tab chosen in the tab argument, instantiates chrome driver, an empty list of dictionaries for storing links and image IDs which may be scrapped using the scrapper <br /> Headless option for running on EC2 instance (True if on EC2 and False if running locally) |
| getPage | Used on instantiation and navigates to tab chosen by user using the tab argument <br /> Toggles cell option added for case when running on EC2 instance, given on local Mac tabs already visible but on EC2 a Menu button would have to be clicked once before tabs are made visible|
| popupEsc | Refreshed driver in the event a popup advertisment shows up, waiting a maximum of 15secs for the advertisement to show up before moving on using selenium's WebDriverWait method |
| getImgs | Yields all iimages on relevant page storing such images into self.img_dict |
| addUUID | Convenience method primarily used in other methods to set UUID using uuid library |
| mkPath | Makes folder raw_data should it not alredy exist |
| mkImgFold | Makes images subfolder within raw_data |
| uploadImg | Uploads images scrapped and stored in img_dict onto images subfolder within raw_data |
| archImg | Creates (if it does not already exist) a json file which shall store json object |
| allLinks | Class method navigating to all possible tabs on Myfxbook homepage, collecting all links existing on each tab and appending them to a list. Finally set operation is applied on the list to yield all unique links  |

### <u>econ_cal_new.py</u> 

<u>Class Name: newsCalendar </u> <br />
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


## Unittest Files (For econ_cal_scraper.py and econ_cal_new.py)
### test_econ_cal_scraper.py 
Unit test file for econ_cal_scraper.py. 

| Method | Description |
| :-- | :-- |
| setUp | Instantiates three instances of EconCalScraper class each navigating to a different tab |
| tearDown | Ensure each instance started up on setUp method |
| test_getImgs | Checks whether the img_dict attribute is of type dict when calling getImgs |
| test_mkFold | Checks the image folder |
| test_getPage | Ensures each class instance is navigated to the current URL on instantiation |
| test_reset | Ensure tab is succesfully set to the one specified in new_tb argument |

### test_econ_cal_new.py
| Method | Description |
| :-- | :-- |
| setUp | Instantiates two instances of newsCalendar class |
| tearDown | Ensure each instance started up on setUp method |
| test_getEvent | Calls and tests the getEvent method which yield a tuple of a list of dictionaries and a dataframe, each containing the same data. The test checks both are of the same length |
| test_tranformData | Ensures on calling the transformData method the list of dictionaries is transformed to a dicionary of list |

## Screenshots/Brief Explanations for EC2 based and Subsequent Tasks
### EC2 Running of Scraper 
Run using commands:
- `sudo docker pull ahmadj8/fx`
- `sudo docker run -it --name fx ahmadj8/fx python econ_cal_new.py`
In order to allow for interaction `-d` flag not applied so container restarted using `sudo docker start fx` whenever required to perform any adhoc commands on instance using `sudo docker exec` <br />
![image](https://user-images.githubusercontent.com/100163231/163238415-236a2800-c6bf-4071-bf91-590b890ca32e.png)
![image](https://user-images.githubusercontent.com/100163231/163238532-1ad7dcf9-73d6-4a18-acc5-b31253274d5b.png)
![image](https://user-images.githubusercontent.com/100163231/163238630-0bb1082b-804f-454d-a1ed-70a0ffca6497.png)


### Prometheus Docker container, node exporter and EC2 instance 
Prometheus container based of prom/prometheus image run on AWS EC2 instance. Running of the Prometheus image contains the following tags:
- `-p 9090:9090` Binding port 9090 on local machine to port 9090 on virtual machine
- `-v /root/prometheus.yml:/etc/prometheus/prometheus.yml` Mounting of file prometheus.yml on local machine to virtual machine
- `-d` Keeps prometheus running in background <br />

![image](https://user-images.githubusercontent.com/100163231/163312129-484711ff-f2f6-47f0-b950-13a2f6aa6266.png)


Configuration for allowing Prometheus to scrape data pertaining to the docker daemon, node exporter running on EC2 instance and prometheus itself (both in the context of local machine and running of an EC2 instance is set out as in the config file below (though public IPv4 address for EC2 will change each time the EC2 instance is restarted) <br />
![image](https://user-images.githubusercontent.com/100163231/163238184-0342dc74-3752-4957-95eb-d75e5e3befbd.png)

The config below pertains to the running of the docker daemon in the background <br />
![image](https://user-images.githubusercontent.com/100163231/163238275-99052ee4-941a-4fca-ac4b-b4363dc73aa8.png)

![image](https://user-images.githubusercontent.com/100163231/163239257-473d456c-6b59-4c25-aefb-ef8004933b79.png)

### s3 Bucket Upload
Used in econ_cal_scrapey.py script but specific function used to upload onto s3, aws_s3_upload, imported from aws_class.py and used to upload images stored in local raw_data > images directory <br />

![image](https://user-images.githubusercontent.com/100163231/163249725-b0e215cb-b600-45da-ab83-f325d745bc97.png)


### RDS Dataupload
Yielded using newCalendar class from econ_cal_new.py. Specifically using the toSql() methods. Please note toSql() already calls the method needed to scrape data from page so no need to run .getEvent() prior in order to scrape information to store into the class instances .df attribute <br />
![image](https://user-images.githubusercontent.com/100163231/163035116-96537d8c-d375-4a47-be59-de3c04418e5f.png)

### Grafana/Node Exporter

Node exporter also set up on local EC2 instance using the following steps in AWS EC2 instance:
- `sudo wget https://github.com/prometheus/node_exporter/releases/download/v*/node_exporter-*.*-amd64.tar.gz`
- `sudo tar -xvf node_exporter-*.*-amd64.tar.gz` : For unzipping node exporter file
- cd into unzipped node file and copy onto local url to view metrics being sent by node:
 `http://<copied-text-from-previous-step>:9100` 

Grafana installed using instructions as set out in official page for mac and accesses using local port 3000 <br />
![image](https://user-images.githubusercontent.com/100163231/163239123-97f55f71-7432-49c2-acec-c6db832d79ca.png)

![image](https://user-images.githubusercontent.com/100163231/163239168-c0c96a0e-85a5-4ae3-a7fd-8a99ad1ef492.png)

### CI-CL Workflow
- Setup new workflow as shown below <br />
![image](https://user-images.githubusercontent.com/100163231/163310673-8b0fe2fa-abcc-4e94-83d8-c8982500840a.png)
![image](https://user-images.githubusercontent.com/100163231/163310700-b9fafc85-361e-48cf-b618-0b60d521285b.png)

- Confirmed workflow succesfully run both manually and on using pushing to remote github repository <br />
<img width="941" alt="image" src="https://user-images.githubusercontent.com/100163231/163310940-d4fa49a1-54ca-4b31-aba2-f403dd5e1ac6.png">


### Crontab Scheduling Process
- Constructed bash script named cron_script.sh running commands as shown below: <br />
 > #!/bin/bash <br />
 > sudo docker rm fx <br />
 > sudo docker pull ahmadj8/fx:latest <br />
 > sudo docker run -it --name fx ahmadj8/fx /bin/bash
- Added execution permission for bash script in EC2 terminal using command `chmod +x cron_script.sh` 
- Checked bash script running correctly using `./con_script.sh` <br />
 ![image](https://user-images.githubusercontent.com/100163231/163310016-4eeddbb5-801f-4cdf-b471-3276682dfa08.png)
- Set up new cron job using command `crontab -e`
- For demonstrative purposes first set the cron job to run every 5minutes <br />
![image](https://user-images.githubusercontent.com/100163231/163310134-887afa7d-4b95-4ca4-beca-ac81c0732700.png)
- Confirmed cron job succesfuly run 5minutes <br />
![image](https://user-images.githubusercontent.com/100163231/163310249-9b2c07b4-fbb9-4663-88a9-f1cdc836010b.png)
- Reset cron job to run every day <br />
![image](https://user-images.githubusercontent.com/100163231/163310299-fe3fd953-50cd-4f9f-90dc-640030a020f7.png)







