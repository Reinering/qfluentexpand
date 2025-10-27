# qfluentwidgets expand

    基于[zhiyiYo](https://github.com/zhiyiYo/PyQt-Fluent-Widgets.git)的UI库进行扩展

## installation 

```bash
    pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.org/simple/
    pip install git+https://github.com/Reinering/qfluentexpand.git@pyside6
```

## usage

## pyside6 designer custom plugin 

### conda environment

```bash
    conda activate myenv
    designer
```
### python

```bash
    cd myenv/scripts
    designer
```

![designer](/public/images/designer.png "designer")



## 自动加载 iconify / simpleicons / 图标库

### iconify 使用
```
    # UI 启动前 加载 初始化
    from qfluentexpand.icongenie.manager import QFluentManager
    
    # 
    iconify = QFluentManager.iconify    # iconify font icon manager
    iconify.setRootPath('./')     # 设置resource文件资源路径， 建议设置项目根目录 创建qrc文件名是固定的：resource/resource_qfe.qrc
    # iconify.setResourcePath("./resources/resource_qfe_rc.py")     # 设置qrc编译后的资源文件路径 不设置时默认: resource_qfe.qrc同路径下resource_qfe_rc.py
    iconify.initialize()
    
    # UI文件中 引用icon
    from qfluentexpand.icongenie.icon import QFluentIcon
    
    QFluentIcon.iconIfy("SETTING")   # 获取google font icon
    # button = PushButton(FluentIcon.SETTING, 'Setting', self)         # 可以将[PyQt-Fluent-Widgets]的FluentIcon
    button = PushButton(QFluentIcon.iconIfy("SETTING"), 'Setting', self)   # 可以将[PyQt-Fluent-Widgets]的FluentIcon 直接替换为QFluentIcon.iconIfy("Setting")
    
```

### simpleicons 使用
```
    # UI 启动前 加载 初始化
    from qfluentexpand.icongenie.manager import QFluentManager
    
    # 
    simpleicons = QFluentManager.simpleicons    # simpleicons font icon manager
    simpleicons.setRootPath('./')     # 设置resource文件资源路径， 建议设置项目根目录 创建qrc文件名是固定的：resource/resource_qfe.qrc
    # simpleicons.setResourcePath("./resources、resource_qfe_rc.py")     # 设置qrc编译后的资源文件路径 不设置时默认: resource_qfe.qrc同路径下resource_qfe_rc.py
    simpleicons.initialize()
    
    # UI文件中 引用icon
    from qfluentexpand.icongenie.icon import QFluentIcon
    
    QFluentIcon.simpleIcons("SETTING")   # 获取google font icon
    # button = PushButton(FluentIcon.SETTING, 'Setting', self)         # 可以将[PyQt-Fluent-Widgets]的FluentIcon
    button = PushButton(QFluentIcon.simpleIcons("SETTING"), 'Setting', self)   # 可以将[PyQt-Fluent-Widgets]的FluentIcon 直接替换为QFluentIcon.simpleIcons("Setting")
    
```

Setting icon 会自动加载 google font icon
所以 QFluentIcon.iconIfy("XXXX") 必须 icon name, 请参考[google font icon](https://fonts.google.com/icons) / [simpleicons](https://simpleicons.org/) / [iconify](https://iconify.design/)

1、第一次运行时，会自动下载icon 到设置的资源路径下 (icon 命名规则: 小写(icon name) + color(hex) + size + '.svg')

![resource](/public/images/resource.png "resource") 

2、下载到的资源，会自动写入qrc文件中，然后自动编译成py文件 文件名：resource_qfe_rc.py

![qrc](/public/images/qrc.png "qrc") 
    
2、编译后，然后重新运行程序，会自动加载到 IconifyIconBase / SimpleIconsIconBase 中

![ui](/public/images/ui.png "ui") 

注意： 

    1、resource_qfe_rc.py 不需要手动引入，模块会自动引入。但打包时，需要注意打包工具配置: 

        1> pyinstaller:  addData: ./resource_qfe_rc.py;./
        2> nuitka:  include-data-files: ./resource_qfe_rc.py=./resource_qfe_rc.py
    2、icon下载是在程序启动开始前期，之后更改并不会触发下载，需要重新启动程序。多主题下，请切换主题后重新启动程序，促使下载新的icon。下载失败，也是需要重新启动程序，重新下载。

### 其他属性设置
```
    # icon color 是根据PyQt-Fluent-Widgets的theme设置的取得颜色hex值
```

### 脚手架 (非嵌入式)

```bash
    icongenie         
```
icongenie 会在根目录下生成icongenie.py 文件

```python
    # icongenie.py
    iconify_icons = [
        ("home", "black", 24),
        ("search", "#2196F3", 32),
    ]

    simpleicons_icons = [
        ("4chan", "black", 24),
        ("aerlingus", "#006272", 32),
    ]
```
将需要的icon添加到对应的列表中，然后运行icongenie.py文件，会自动下载到设置的资源路径下

```bash
    python icongenie.py
```
使用资源路径下的icon，可以查看resources/resource_qfe.qrc文件

```python
    QIcon(":/app/iconify/icons/home_black_24.svg")
    QIcon(":/app/simpleicons/icons/4chan_black_24.svg")
```



## reference
[zhiyiYo](https://github.com/zhiyiYo/PyQt-Fluent-Widgets.git)
