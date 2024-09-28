#!/usr/bin/env bash




qfluentexpand=Lib/site-packages/qfluentexpand

cd ../../../..


# DISPLAY=

# 设置引用路径问
# LD_LIBRARY_PATH=

# QML2_IMPORT_PATH=

# 开启Qt debug
export QT_DEBUG_PLUGINS=1

export PYSIDE_DESIGNER_PLUGINS=${qfluentexpand}/plugins/qfluentexpand;${qfluentexpand}/plugins

python ${qfluentexpand}/tools/pyside6-designer.py -p %PYSIDE_DESIGNER_PLUGINS% %1
