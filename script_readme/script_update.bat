@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate one folder up for target folders
set "targetFolder1=..\VSDSquadron_Mini"
set "targetFolder2=..\VSDSquadron_FM"
set "targetFolder3=..\VSDSquadron_Pro"
set "targetFolder4=..\VSDSquadron_Ultra"
set "targetFolder5=..\VSDSquadron_SKY130"

REM Navigate two folders up for source folders
set "sourceFolder1=..\..\PCB_VSDSquadron_Mini\squadron_mini\production"
set "sourceFolder2=..\..\PCB_VSDSquadron_FM\squadron_FM\production"
set "sourceFolder3=..\..\PCB_VSDSquadron_Pro\squadron_pro\production"
set "sourceFolder4=..\..\PCB_VSDSquadron_Ultra\squadron_ultraA\production"
set "sourceFolder5=..\..\PCB_VSDSquadron_SKY130\squadron_sky130\production"

REM Clear existing .jpg and .pdf files from target folders
del /q "%targetFolder1%\*.jpg"
del /q "%targetFolder1%\*.pdf"
del /q "%targetFolder2%\*.jpg"
del /q "%targetFolder2%\*.pdf"
del /q "%targetFolder3%\*.jpg"
del /q "%targetFolder3%\*.pdf"
del /q "%targetFolder4%\*.jpg"
del /q "%targetFolder4%\*.pdf"
del /q "%targetFolder5%\*.jpg"
del /q "%targetFolder5%\*.pdf"


REM Copy .jpg and .pdf files from source to target folders
xcopy "%sourceFolder1%\*.jpg" "%targetFolder1%\" /s /y
xcopy "%sourceFolder1%\*.pdf" "%targetFolder1%\" /s /y

xcopy "%sourceFolder2%\*.jpg" "%targetFolder2%\" /s /y
xcopy "%sourceFolder2%\*.pdf" "%targetFolder2%\" /s /y

xcopy "%sourceFolder3%\*.jpg" "%targetFolder3%\" /s /y
xcopy "%sourceFolder3%\*.pdf" "%targetFolder3%\" /s /y

xcopy "%sourceFolder4%\*.jpg" "%targetFolder4%\" /s /y
xcopy "%sourceFolder4%\*.pdf" "%targetFolder4%\" /s /y

xcopy "%sourceFolder5%\*.jpg" "%targetFolder5%\" /s /y
xcopy "%sourceFolder5%\*.pdf" "%targetFolder5%\" /s /y

REM Push all changes
cd ..
git add .
git commit -m "Updated production folders"
git push

REM Return to the original directory
cd "%original_dir%"
echo Done.
