@echo off
REM Save the current directory
set "original_dir=%cd%"

REM Navigate one folder up for target folders
set "targetFolder1=..\VSDSquadronMini_CH32V003"
set "targetFolder2=..\VSDSquadron_gf180"
set "targetFolder3=..\VSDSquadron_openMPW"
set "targetFolder4=..\VSDSquadronMini_programmer"
set "targetFolder5=..\VSDSquadron_FM"
set "targetFolder6=..\VSDSquadron_sifive"

REM Navigate two folders up for source folders
set "sourceFolder1=..\..\squadron_CH32\SquadronMini_2B\production"
set "sourceFolder2=..\..\squadron_GF180\squadron_GF180_1A\production"
set "sourceFolder3=..\..\squadron_MPW\squadron-4A\production"
set "sourceFolder4=..\..\squadron_CH32\Mini_Programmer_1A\production"
set "sourceFolder5=..\..\squadron_lattice\squadron_FM_4A\production"
set "sourceFolder6=..\..\squadron_sifive\squadron_sifive_1B\production"

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
del /q "%targetFolder6%\*.jpg"
del /q "%targetFolder6%\*.pdf"

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

xcopy "%sourceFolder6%\*.jpg" "%targetFolder6%\" /s /y
xcopy "%sourceFolder6%\*.pdf" "%targetFolder6%\" /s /y

REM Push all changes
cd ..
git add .
git commit -m "Updated production folders"
git push

REM Return to the original directory
cd "%original_dir%"
echo Done.
