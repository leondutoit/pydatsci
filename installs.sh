#!/bin/bash

sudo apt-get update
sudo apt-get -y install git gcc emacs
sudo apt-get update
sudo apt-get install -y python-pip python-dev libyaml-dev g++ sqlite3
sudo apt-get install -y automake python-setuptools python-software-properties
sudo apt-get install -y libatlas-base-dev gfortran build-essential
sudo pip install numpy pandas flask ipython nose statsmodels
sudo apt-get install -y python-scipy
sudo apt-get install -y python-matplotlib
sudo pip install ggplot

./test.sh
