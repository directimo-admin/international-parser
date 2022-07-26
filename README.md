
# DIRECTIMO-CONDO-PARSER

This tool will be used to crawl and extract data from condo oriented websites

## Requirements
You should have the following tools installed on your machine:  
Python ~ 3.8  
Pip3 ~ 21.1.2  
Docker ~ 20.10.8  
Docker-compose ~ 1.29.2   

Other than python you will need a key to Zyte Proxy provider.

## Installation

Install the following dependencies (inside project root folder):
```sh
pip3 install -r requirements.txt &
pip3 install git+https://github.com/iamumairayub/scrapyd-client.git --upgrade
```




## Configuration

Create the following directories:
```
~/db/mongo
~/db/sql
~/condo-reports
```

Open condoparser/settings.py and replace ZYTE_SMARTPROXY_APIKEY with your Zyte key

**If you are using a M1 Macbook, add ```platform: linux/amd64``` in ```services/docker-compose.yml```  under ```mysql-db```

## Deployment

In order to deploy you have to run (inside project root folder):

``` docker-compose  --env-file .env.local up -d```

Now you need to deploy the spiders:
```scrapyd-deploy```

## Run

There are few files with different output, they must be ran in the order below

To get the data from websites and save it to Mongo, run (in run project): 

```python3 startScrapyWorkers.py imobiliare```

## License
GNU General Public License v3.0 or later

See LICENSE to see the full text.
