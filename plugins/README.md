# pyside6-designer 插件



### 第一步 写插件


### 第二步 在register.py中注册插件

```python


### 注意 PluginBase 的__init__方法中的, 必须调用super().__init__(parent)方法, 否则会报错