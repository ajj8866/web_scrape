# syntax=docker/dockerfile:1

FROM python:3.8

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
    && apt-get -y update\
    && apt-get install -y wget \
    && apt-get install -y google-chrome-stable 

WORKDIR ./app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "econ_cal_scraper.py"]


# # 2. Adding trusting keys to apt for repositories, you can download and add them using the following command:
# wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# # 3. Add Google Chrome. Use the following command for that
# sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# # 4. Update apt:
# apt-get -y update

# # 5. And install google chrome:
# apt-get install -y google-chrome-stable

# FROM python:3.8

# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
#     && apt-get -y update\
#     && apt-get install -y google-chrome-stable
    
# COPY . .

# RUN pip install -r requirements.txt

# CMD ["python", "econ_cal_scraper.py"]
