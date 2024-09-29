@echo off 
cls 
echo off
echo. 
echo ----------------------------开启designer----------------------------

set qfluentexpand=Lib\site-packages\qfluentexpand

cd /d %~dp0../../../..

::SET DISPLAY

:: 设置引用路径问
::SET LD_LIBRARY_PATH

::SET QML2_IMPORT_PATH

:: 开启Qt debug
SET QT_DEBUG_PLUGINS=1

SET PYSIDE_DESIGNER_PLUGINS=%qfluentexpand%\plugins\expand;%qfluentexpand%\plugins

python %qfluentexpand%\tools\designer.py -p %PYSIDE_DESIGNER_PLUGINS% %1
