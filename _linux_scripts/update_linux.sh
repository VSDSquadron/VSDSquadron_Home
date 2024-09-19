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
targetFolder1="squadron_production/VSDSquadronMini_CH32V003"
targetFolder2="squadron_production/VSDSquadron_gf180"
targetFolder3="squadron_production/VSDSquadron_openMPW"
targetFolder4="squadron_production/VSDSquadronMini_programmer"
targetFolder5="squadron_production/VSDSquadron_FM"
targetFolder6="squadron_production/VSDSquadron_sifive"

# Set the paths for the Target folder
targetFolder1Path="$rootPath$targetFolder1"
targetFolder2Path="$rootPath$targetFolder2"
targetFolder3Path="$rootPath$targetFolder3"
targetFolder4Path="$rootPath$targetFolder4"
targetFolder5Path="$rootPath$targetFolder5"
targetFolder6Path="$rootPath$targetFolder6"

# Copy the contents of the production folder from each sub-folder to the new folder
cp -r "$sourceFolder1Path/production"/* "$targetFolder1Path"
cp -r "$sourceFolder2Path/production"/* "$targetFolder2Path"
cp -r "$sourceFolder3Path/production"/* "$targetFolder3Path"
cp -r "$sourceFolder4Path/production"/* "$targetFolder4Path"
cp -r "$sourceFolder5Path/production"/* "$targetFolder5Path"
cp -r "$sourceFolder6Path/production"/* "$targetFolder6Path"
