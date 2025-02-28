@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate two folders up
cd ..\..

REM List of repositories to clone
set repos=PCB_VSDSquadron_Pro PCB_VSDSquadron_Mini PCB_VSDSquadron_FM PCB_VSDSquadron_Ultra PCB_VSDSquadron_SKY130

REM GitHub username
set username=VSDSquadron

REM Loop through each repository and clone it
for %%r in (%repos%) do (
    echo Cloning repository %%r...
    git clone --recursive https://github.com/%username%/%%r.git
)

REM Return to the original directory
cd "%original_dir%"
echo Done.
