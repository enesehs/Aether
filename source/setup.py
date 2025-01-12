"""
Author: enesehs
Builder: cx_Freeze
Build Script: build.py
Build Command: python build.py build
License: GNU General Public License v3.0
"""

from cx_Freeze import setup, Executable
import os

build_options = {
    'packages': ['os', 'sys', 'tkinter'],
    'excludes': ['unittest'],
    'include_files': [
        ('img', 'img'),
        ('sound', 'sound'),
        ('settings.enc', 'settings.enc'),
        ('settings.key', 'settings.key'),
        ('settings.ini', 'settings.ini')
    ],
}

icon_path = os.path.abspath('C:/Users/Admin/Desktop/ProjetAether2/img/main.ico')

executables = [
    Executable(
        script='NewGUI.py',
        base='Win32GUI',
        icon=icon_path,
        target_name='Aether.exe'
    )
]

setup(
    name='Aether',
    version='0.1',
    description='Pre-Relase',
    options={'build_exe': build_options},
    executables=executables
)





