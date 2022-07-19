#!/bin/bash
source ~/.bash_profile &&
cd /home/bb-user/code &&
/usr/local/bin/scrapyd-deploy &&
/usr/bin/python3 startScrapyWorkers.py Imobiliare &&
/usr/bin/python3 processDataIntoDB.py &&
/usr/bin/python3 generateResults.py