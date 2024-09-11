# pyside6 designer qfluentexpand 插件



### 第一步 写插件


### 第二步 在register.py中注册插件

```python


### 注意 
1、PluginBase 的__init__方法中的, 必须调用super().__init__(parent)方法, 否则会报错
2、register中的插件路径要根据目录改为绝对路径