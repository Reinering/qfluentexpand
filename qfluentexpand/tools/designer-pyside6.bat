@echo off 
cls 
echo off
echo. 
echo ----------------------------����designer----------------------------

set qfluentexpand=Lib\site-packages\qfluentexpand

cd /d %~dp0../../../..

::SET DISPLAY

:: ��������·����
::SET LD_LIBRARY_PATH

::SET QML2_IMPORT_PATH

:: ����Qt debug
SET QT_DEBUG_PLUGINS=1

SET PYSIDE_DESIGNER_PLUGINS=%qfluentexpand%\plugins\expand;%qfluentexpand%\plugins

python %qfluentexpand%\tools\designer.py -p %PYSIDE_DESIGNER_PLUGINS% %1
