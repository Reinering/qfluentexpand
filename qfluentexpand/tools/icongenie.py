#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""


# from qfluentexpand.common import iconGenie
import os
import sys


def createFile():
    example = os.path.join('Lib', 'site-packages', 'qfluentexpand', 'icongenie', 'example.py')
    (filepath, filename) = os.path.split(sys.executable)

    if not os.path.exists('icongenie.py'):
        cmd = f"copy {os.path.join(filepath, example)} icongenie.py"
        os.system(cmd)


def main():
    print("Please confirm whether it is in the project root directory")
    result = ''
    while True:
        result = input("confirm: (Y/N)")
        if result.lower() == 'y':
            break
        elif result.lower() == 'n':
            return
        else:
            print("Please enter y or n")

    print('IconGenie')
    print('create resources folder')
    createFile()





    print('IconGenie finished')





if __name__ == '__main__':
    main()