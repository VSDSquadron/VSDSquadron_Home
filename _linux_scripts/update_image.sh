#!/bin/bash

# Set the root path for all 6 folders
rootPath="../"

# Set individual Source folder names
sourceFolder1="squadron_CH32/SquadronMini_2A"
sourceFolder2="squadron_GF180/squadron_GF180_1A"
sourceFolder3="squadron_MPW/squadron-3A"
sourceFolder4="squadron_CH32/Mini_Programmer_1A"
sourceFolder5="squadron_lattice/squadron_FM_2A"
sourceFolder6="squadron_sifive/squadron_sifive_1A"

# Set the paths for the first 6 folders
sourceFolder1Path="$rootPath$sourceFolder1"
sourceFolder2Path="$rootPath$sourceFolder2"
sourceFolder3Path="$rootPath$sourceFolder3"
sourceFolder4Path="$rootPath$sourceFolder4"
sourceFolder5Path="$rootPath$sourceFolder5"
sourceFolder6Path="$rootPath$sourceFolder6"

# Set individual Target folder names
targetFolder1="VSDSquadron/VSDSquadronMini_CH32V003"
targetFolder2="VSDSquadron/VSDSquadron_gf180"
targetFolder3="VSDSquadron/VSDSquadron_openMPW"
targetFolder4="VSDSquadron/VSDSquadronMini_programmer"
targetFolder5="VSDSquadron/VSDSquadron_FM"
targetFolder6="VSDSquadron/VSDSquadron_sifive"

# Set the paths for the Target folder
targetFolder1Path="$rootPath$targetFolder1"
targetFolder2Path="$rootPath$targetFolder2"
targetFolder3Path="$rootPath$targetFolder3"
targetFolder4Path="$rootPath$targetFolder4"
targetFolder5Path="$rootPath$targetFolder5"
targetFolder6Path="$rootPath$targetFolder6"

# Copy the contents of the production folder from each sub-folder to the new folder
cp -r "$sourceFolder1Path/production"/*.jpg "$targetFolder1Path"
cp -r "$sourceFolder2Path/production"/*.jpg "$targetFolder2Path"
cp -r "$sourceFolder3Path/production"/*.jpg "$targetFolder3Path"
cp -r "$sourceFolder4Path/production"/*.jpg "$targetFolder4Path"
cp -r "$sourceFolder5Path/production"/*.jpg "$targetFolder5Path"
cp -r "$sourceFolder6Path/production"/*.jpg "$targetFolder6Path"

cd ../VSDSquadron/

git add .
git commit -m "update images"
git push 

cd ../squadron_production