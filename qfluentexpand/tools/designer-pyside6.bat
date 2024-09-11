@echo off 
cls 
echo off
echo. 
echo ----------------------------开启designer---------------------------- 

SET PYENV=pyside6

::SET DISPLAY

:: 设置引用路径问
::SET LD_LIBRARY_PATH

::
::SET QML2_IMPORT_PATH

:: 开启Qt debug
SET QT_DEBUG_PLUGINS=1

SET PYSIDE_DESIGNER_PLUGINS=D:\Tools\Designer-Plugin\qfluentexpand\plugins\pyside6;D:\Tools\Designer-Plugin\qfluentwidgets\PySide6\PySide6-Fluent-Widget\plugins

call conda activate %PYENV%

python %~dp0pyside6-designer.py -p %PYSIDE_DESIGNER_PLUGINS% %1

::exit
