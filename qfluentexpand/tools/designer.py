#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
"""
author: Reiner
email: nbxlc@hotmail.com
"""


import os
import sys
import time
import argparse
import getopt
import subprocess
import importlib
import sysconfig
from pathlib import Path

import PySide6 as ref_mod

VIRTUAL_ENV = "VIRTUAL_ENV"
pyside_dir = Path(ref_mod.__file__).resolve().parent

ARGV = sys.argv[1:]

def is_pyenv_python():
    pyenv_root = os.environ.get("PYENV_ROOT")

    if pyenv_root:
        resolved_exe = Path(sys.executable).resolve()
        if str(resolved_exe).startswith(pyenv_root):
            return True

    return False


def is_virtual_env():
    return sys.prefix != sys.base_prefix


def init_virtual_env():
    """PYSIDE-2251: Enable running from a non-activated virtual environment
       as is the case for Visual Studio Code by setting the VIRTUAL_ENV
       variable which is used by the Qt Designer plugin."""
    if is_virtual_env() and not os.environ.get(VIRTUAL_ENV):
        os.environ[VIRTUAL_ENV] = sys.prefix


def main1():
    # This will take care of "pyside6-lupdate" listed as an entrypoint
    # in setup.py are copied to 'scripts/..'
    cmd = os.path.join("", os.path.basename(sys.argv[0]))
    command = [os.path.join(os.path.dirname(os.path.realpath(__file__)), cmd)]
    command.extend(ARGV)
    sys.exit(subprocess.call(command))


def qt_tool_wrapper(qt_tool, args, libexec=False):
    # Taking care of pyside6-uic, pyside6-rcc, and pyside6-designer
    # listed as an entrypoint in setup.py

    if libexec and sys.platform != "win32":
        exe = pyside_dir / 'Qt' / 'libexec' / qt_tool
    else:
        exe = pyside_dir / qt_tool

    cmd = [os.fspath(exe)] + args
    print("cmd", cmd)
    while True:
        startTime = time.time()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if err:
            msg = err.decode("utf-8")
            command = ' '.join(cmd)
            print(f"Error: {msg}\nwhile executing '{command}'")
        print(out.decode("gbk"))

        count = time.time() - startTime
        if count > 10:
            sys.exit(proc.returncode)


def pyside_script_wrapper(script_name):
    """Launch a script shipped with PySide."""
    script = Path(__file__).resolve().parent / script_name
    command = [sys.executable, os.fspath(script)] + ARGV
    sys.exit(subprocess.call(command))


def ui_tool_binary(binary):
    """Return the binary of a UI tool (App bundle on macOS)."""
    if sys.platform != "darwin":
        return binary
    name = binary[0:1].upper() + binary[1:]
    return f"{name}.app/Contents/MacOS/{name}"


def lrelease():
    qt_tool_wrapper("lrelease", ARGV)


def lupdate():
    qt_tool_wrapper("lupdate", ARGV)


def uic():
    qt_tool_wrapper("uic", ['-g', 'python'] + ARGV, True)


def rcc():
    args = []
    user_args = ARGV
    if "--binary" not in user_args:
        args.extend(['-g', 'python'])
    args.extend(user_args)
    qt_tool_wrapper("rcc", args, True)


def qmltyperegistrar():
    qt_tool_wrapper("qmltyperegistrar", ARGV, True)


def qmlimportscanner():
    qt_tool_wrapper("qmlimportscanner", ARGV, True)


def qmlcachegen():
    qt_tool_wrapper("qmlcachegen", ARGV, True)


def qmllint():
    qt_tool_wrapper("qmllint", ARGV)


def qmlformat():
    qt_tool_wrapper("qmlformat", ARGV)


def qmlls():
    qt_tool_wrapper("qmlls", ARGV)


def assistant():
    qt_tool_wrapper(ui_tool_binary("assistant"), ARGV)


def _extend_path_var(var, value, prepend=False):
    print(var, value)
    env_value = os.environ.get(var)
    if env_value:
        env_value = (f'{value}{os.pathsep}{env_value}'
                     if prepend else f'{env_value}{os.pathsep}{value}')
    else:
        env_value = value
    os.environ[var] = env_value


def designer():
    print("designer starting")

    init_virtual_env()

    # https://www.python.org/dev/peps/pep-0384/#linkage :
    # "On Unix systems, the ABI is typically provided by the python executable
    # itself", that is, libshiboken does not link against any Python library
    # and expects to get these symbols from a python executable. Since no
    # python executable is involved when loading this plugin, pre-load python.so
    # This should also help to work around a numpy issue, see
    # https://stackoverflow.com/questions/49784583/numpy-import-fails-on-multiarray-extension-library-when-called-from-embedded-pyt
    major_version = sys.version_info[0]
    minor_version = sys.version_info[1]
    os.environ['PY_MAJOR_VERSION'] = str(major_version)
    os.environ['PY_MINOR_VERSION'] = str(minor_version)
    if sys.platform == 'linux':
        # Determine library name (examples/utils/pyside_config.py)
        version = f'{major_version}.{minor_version}'
        library_name = f'libpython{version}{sys.abiflags}.so'
        if is_pyenv_python():
            library_name = str(Path(sysconfig.get_config_var('LIBDIR')) / library_name)
        os.environ['LD_PRELOAD'] = library_name
    elif sys.platform == 'darwin':
        library_name = sysconfig.get_config_var("LDLIBRARY")
        framework_prefix = sysconfig.get_config_var("PYTHONFRAMEWORKPREFIX")
        lib_path = None
        if framework_prefix:
            lib_path = os.fspath(Path(framework_prefix) / library_name)
        elif is_pyenv_python():
            lib_path = str(Path(sysconfig.get_config_var('LIBDIR')) / library_name)
        else:
            # ideally this should never be reached because the system Python and Python installed
            # from python.org are all framework builds
            print("Unable to find Python library directory. Use a framework build of Python.",
                  file=sys.stderr)
            sys.exit(0)
        os.environ['DYLD_INSERT_LIBRARIES'] = lib_path
    elif sys.platform == 'win32':
        # Find Python DLLs from the base installation
        if is_virtual_env():
            _extend_path_var("PATH", os.fspath(Path(sys._base_executable).parent), True)

    qt_tool_wrapper(ui_tool_binary("designer"), ARGV)


def linguist():
    qt_tool_wrapper(ui_tool_binary("linguist"), ARGV)


def genpyi():
    pyside_dir = Path(__file__).resolve().parents[1]
    support = pyside_dir / "support"
    cmd = support / "generate_pyi.py"
    command = [sys.executable, os.fspath(cmd)] + ARGV
    sys.exit(subprocess.call(command))


def metaobjectdump():
    pyside_script_wrapper("metaobjectdump.py")


def project():
    pyside_script_wrapper("project.py")


def qml():
    pyside_script_wrapper("qml.py")


def qtpy2cpp():
    pyside_script_wrapper("qtpy2cpp.py")


def deploy():
    pyside_script_wrapper("deploy.py")


def android_deploy():
    if not sys.platform == "linux":
        print("pyside6-android-deploy only works from a Linux host")
    else:
        android_requirements_file = Path(__file__).parent / "requirements-android.txt"
        with open(android_requirements_file, 'r', encoding='UTF-8') as file:
            while line := file.readline():
                dependent_package = line.rstrip()
                if not bool(importlib.util.find_spec(dependent_package)):
                    command = [sys.executable, "-m", "pip", "install", dependent_package]
                    subprocess.run(command)
        pyside_script_wrapper("android_deploy.py")


def qsb():
    qt_tool_wrapper("qsb", ARGV)


def balsam():
    qt_tool_wrapper("balsam", ARGV)


def balsamui():
    qt_tool_wrapper("balsamui", ARGV)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(*argv,  **kwargs):
    if not argv:
        argv = sys.argv[1:]

    try:
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('-p', '--plugin', nargs='*', action='store', help='add plugin path')
            # args = parser.parse_args()
            # args, unknown = parser.parse_known_args(argv)
            # print(args, unknown)

            known_args = []
            unknown_args = []

            i = 0
            while i < len(argv):
                if argv[i] in ['-p', '--plugin']:
                    if i + 1 < len(argv):
                        known_args.extend([argv[i], argv[i + 1]])
                        i += 2
                    else:
                        known_args.append(argv[i])
                        i += 1
                else:
                    unknown_args.append(argv[i])
                    i += 1

            # 使用 parse_known_args 来处理其他已知参数
            args, _ = parser.parse_known_args(known_args)

            # print("已知参数:", args)
            # print("未知参数:", unknown_args)

            global ARGV
            ARGV = unknown_args
            if args.plugin:
                _extend_path_var('PYSIDE_DESIGNER_PLUGINS', args.plugin[0])
            else:
                pluginPath = pyside_dir / '..' / 'qfluentexpand' / 'plugins'
                _extend_path_var('PYSIDE_DESIGNER_PLUGINS', str(pluginPath / 'expand') + ';' + str(pluginPath))

            designer()


        except getopt.error as msg:
            raise Usage(msg)
    except Usage as err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2




if __name__ == "__main__":
    # print("pyside_dir", pyside_dir)
    main()
