@echo off

REM Set the root path for all 6 folders
set "rootPath=C:\project_VSD\VSDSQUADRON\"

REM Set individual Source folder names
set "sourceFolder1=squadron_CH32\SquadronMini_2A"
set "sourceFolder2=squadron_GF180\squadron_GF180_1A"
set "sourceFolder3=squadron_MPW\squadron-4A"
set "sourceFolder4=squadron_CH32\Mini_Programmer_1A"
set "sourceFolder5=squadron_lattice\squadron_FM_2A"
set "sourceFolder6=squadron_sifive\squadron_sifive_1A"

REM Set the paths for the first 6 folders
set "sourceFolder1Path=%rootPath%%sourceFolder1%"
set "sourceFolder2Path=%rootPath%%sourceFolder2%"
set "sourceFolder3Path=%rootPath%%sourceFolder3%"
set "sourceFolder4Path=%rootPath%%sourceFolder4%"
set "sourceFolder5Path=%rootPath%%sourceFolder5%"  
set "sourceFolder6Path=%rootPath%%sourceFolder6%"  

REM Set individual Target folder names
set "targetFolder1=vsdsquadron_production\VSDSquadronMini_CH32V003"
set "targetFolder2=vsdsquadron_production\VSDSquadron_gf180"
set "targetFolder3=vsdsquadron_production\VSDSquadron_openMPW"
set "targetFolder4=vsdsquadron_production\VSDSquadronMini_programmer"
set "targetFolder5=vsdsquadron_production\VSDSquadron_FM"
set "targetFolder6=vsdsquadron_production\VSDSquadron_sifive"

REM Set the path for the Target folder
set "targetFolder1Path=%rootPath%%targetFolder1%"
set "targetFolder2Path=%rootPath%%targetFolder2%"
set "targetFolder3Path=%rootPath%%targetFolder3%"
set "targetFolder4Path=%rootPath%%targetFolder4%"
set "targetFolder5Path=%rootPath%%targetFolder5%"
set "targetFolder6Path=%rootPath%%targetFolder6%"

REM Copy the contents of the production folder from each sub-folder to the new folder
xcopy /E /I "%sourceFolder1Path%\production\*" "%targetFolder1Path%"
xcopy /E /I "%sourceFolder2Path%\production\*" "%targetFolder2Path%"
xcopy /E /I "%sourceFolder3Path%\production\*" "%targetFolder3Path%"
xcopy /E /I "%sourceFolder4Path%\production\*" "%targetFolder4Path%"
xcopy /E /I "%sourceFolder5Path%\production\*" "%targetFolder5Path%"
xcopy /E /I "%sourceFolder6Path%\production\*" "%targetFolder6Path%"

echo Contents copied successfully to %targetFolder1Path%, %targetFolder2Path%, %targetFolder3Path%, %targetFolder4Path%, %targetFolder5Path%, and %targetFolder6Path%.

REM Push all changes
git add .
git commit -m "Updated production folders"
git push

echo Changes pushed successfully.
