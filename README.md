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



### 自动加载 google font icon

```
    # UI 启动前 加载 初始化
    from qfluentexpand.icongenie.manager import QFluentManager
    
    # 
    material = QFluentManager.google    # google font icon manager
    material.setRootPath(ROOT_PATH)     # 设置resource文件资源路径， 建议设置项目根目录 创建qrc文件名是固定的：resource_qfe.qrc
    material.setResourcePath(os.path.join(ROOT_PATH, "resource_qfe_rc.py"))     # 设置qrc编译后的资源文件路径 比如 ./resource_qfe_rc.py
    material.init()
    
    # UI文件中 引用icon
    from qfluentexpand.icongenie.icon import QFluentIcon
    
    QFluentIcon.googleIcon("SETTING")   # 获取google font icon
    # button = PushButton(FluentIcon.SETTING, 'Setting', self)         # 可以将[PyQt-Fluent-Widgets]的FluentIcon
    button = PushButton(QFluentIcon.googleIcon("SETTING"), 'Setting', self)   # 可以将[PyQt-Fluent-Widgets]的FluentIcon 直接替换为QFluentIcon.googleIcon("Setting")
    
```
Setting icon 会自动加载 google font icon
所以 QFluentIcon.googleIcon("XXXX") 必须 google font icon name, 请参考[google font icon](https://fonts.google.com/icons)

1、第一次运行时，会自动下载google font icon 到设置的资源路径下 (icon 命名规则: 小写(google font icon name) + color(hex) + size + '.svg')

![resource](/public/images/resource.png "resource") 

2、下载到的资源，会自动写入qrc文件中，然后编译成py文件（暂时还需要手动编译）

![qrc](/public/images/qrc.png "qrc") 
    
2、编译后，然后重新运行程序，会自动加载到 GoogleMaterialIconBase 中，QFluentIcon.googleIcon("SETTING")调用也是从GoogleMaterialIconBase获取的

![ui](/public/images/ui.png "ui") 

### 其他属性设置
```
    # icon size
    material.setSize(32)    # 设置获取google font icon size
    
    # icon color 是根据PyQt-Fluent-Widgets的theme设置的取得颜色hex值

```



## reference
[zhiyiYo](https://github.com/zhiyiYo/PyQt-Fluent-Widgets.git)
