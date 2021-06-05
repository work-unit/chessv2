#!/bin/bash
#Create Environment
conda env create -f environment.yml
conda activate grand_master
jupyter lab
