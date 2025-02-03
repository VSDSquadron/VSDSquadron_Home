@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate two folders up
cd ..\..

REM List of repositories to push
set repos=squadron_CH32 squadron_GF180 squadron_MPW squadron_lattice squadron_sifive squadron_lib squadron_Riscduino squadron_tejas32

REM Loop through each repository and push changes
for %%r in (%repos%) do (
    REM Check if the directory exists
    if exist %%r (
        echo Committing and pushing changes for repository %%r...
        cd %%r
        
        REM Add all changes
        git add --all
        
        REM Commit changes with the specified message
        git commit -m "Batch updating from home repository"
        
        REM Push changes to the remote repository
        git push

        cd ..
    ) else (
        echo Repository %%r does not exist. Skipping...
    )
)

REM Return to the original directory
cd "%original_dir%"
echo Done.
