#!/usr/bin/env bash




qfluentexpand=Lib/site-packages/qfluentexpand

cd ../../../..


# DISPLAY=

# ��������·����
# LD_LIBRARY_PATH=

# QML2_IMPORT_PATH=

# ����Qt debug
export QT_DEBUG_PLUGINS=1

export PYSIDE_DESIGNER_PLUGINS=${qfluentexpand}/plugins/qfluentexpand;${qfluentexpand}/plugins

python ${qfluentexpand}/tools/pyside6-designer.py -p %PYSIDE_DESIGNER_PLUGINS% %1
