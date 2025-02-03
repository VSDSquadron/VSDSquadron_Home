@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate two folders up
cd ..\..

REM List of repositories to clone
set repos=squadron_CH32 squadron_GF180 squadron_MPW squadron_lattice squadron_sifive squadron_lib squadron_Riscduino squadron_tejas32

REM GitHub username
set username=yathAg

REM Loop through each repository and clone it
for %%r in (%repos%) do (
    echo Cloning repository %%r...
    git clone --recursive https://github.com/%username%/%%r.git
)

REM Return to the original directory
cd "%original_dir%"
echo Done.
