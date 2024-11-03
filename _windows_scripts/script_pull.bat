@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate two folders up
cd ..\..

REM List of repositories to pull
set repos=squadron_CH32 squadron_GF180 squadron_MPW squadron_lattice squadron_sifive squadron_lib squadron_Riscduino

REM Loop through each repository and pull the latest changes including submodules
for %%r in (%repos%) do (
    REM Check if the directory exists
    if exist %%r (
        echo Pulling latest changes for repository %%r including submodules...
        cd %%r
        git pull --recurse-submodules
        REM Update submodules to the latest commit on their respective branches
        git submodule update --remote --merge
        cd ..
    ) else (
        echo Repository %%r does not exist. Skipping...
    )
)

REM Return to the original directory
cd "%original_dir%"
echo Done.
