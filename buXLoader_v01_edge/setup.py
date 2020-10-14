import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "shutil", "subprocess", "tkinter",
                                  "threading", "tkinter.filedialog", "time", "bs4", "requests", "re", "selenium"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="BuXLoader-Edge",
      version="0.1",
      description="BuX Downloader for Edge",
      options={"build_exe": build_exe_options},
      executables=[Executable("BuXLoader.pyw", base=base)])
