#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner
email: nbxlc@hotmail.com
"""


def main():
    import os
    from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
    plugins = []

    def get_modules(py):
        from PySide6.QtDesigner import QDesignerCustomWidgetInterface
        import inspect

        modules = []
        for name, obj in inspect.getmembers(py, inspect.isclass):
            if name.endswith('Plugin'):
                obj = obj()
                # print(name, isinstance(obj, QDesignerCustomWidgetInterface))
                if isinstance(obj, QDesignerCustomWidgetInterface):
                    print(f"Loading {name}")
                    modules.append(obj)
        return modules

    try:
        print("registering widgets")
        for filename in os.listdir(''):        # 路径需要根据插件目录改为绝对路径
            # print("filename", filename)
            if filename.endswith('.py') and not filename.startswith('_'):
                # plugins += get_modules(__import__(f"{filename}".replace('.py', '')))

                py = __import__(f"{filename}".replace('.py', ''))
                for plug in get_modules(py):
                    QPyDesignerCustomWidgetCollection.addCustomWidget(plug)
        print("Widgets registered")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()