#!/bin/bash
http_user=$1
http_password=$2
sudo apt update &
sudo apt install software-properties-common &
sudo add-apt-repository ppa:deadsnakes/ppa -y &
sudo kill -9 $(sudo lsof -t -i:9000)
echo "Installing packages"

REQUIRED_PACKAGES=(python3.8 python3-pip python-dev docker.io docker-compose)
for package in ${REQUIRED_PACKAGES[@]}

do
        sudo apt --assume-yes install $package &

done &
wait

 echo "Installing python dependencies"
 pip install -r ../requirements.txt &
 pip install git+https://github.com/iamumairayub/scrapyd-client.git --upgrade
 export PARSER_REPORT_LOCATION=/mnt/volume_lon1_01/reports
 export PROXY_PATH=/mnt/volume_lon1_01/condo-proxy
 export HTTP_PASSWORD=$http_password
 export HTTP_USER=$http_user
wait
  echo "Start and deploy report http server"
  cd /mnt/volume_lon1_01/reports
  nohup python3 /home/bb-user/code/services/reports_server.py $http_user $http_password &
  cd /home/bb-user/code/services

 echo "Start and deploy docker containers"
 sudo systemctl start docker
 docker stop $(docker ps -a -q)
 docker-compose  --env-file .config/.env.staging up -d --build

