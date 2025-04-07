# import sys
import subprocess
import os
import platform
import bpy


def is_windows():
    return os.name == 'nt'


def is_macos():
    return os.name == 'posix' and platform.system() == "Darwin"


def is_linux():
    return os.name == 'posix' and platform.system() == "Linux"


def python_exec():
    if is_windows():
        import sys
        return os.path.join(sys.prefix, 'bin', 'python.exe')
    elif is_macos():
        import sys
        try:
            # 2.92 and older
            path = bpy.app.binary_path_python
        except AttributeError:
            # 2.93 and later
            path = sys.executable
        return os.path.abspath(path)
    elif is_linux():
        import sys
        return os.path.join(sys.prefix, 'bin', 'python3.11')
    else:
        print("sorry, still not implemented for ", os.name, " - ", platform.system)


def install_modules(packages):
    python_exe = python_exec()

    try:
        # upgrade pip
        subprocess.call([python_exe, "-m", "ensurepip"])
        subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
        # install required packages
        subprocess.call([python_exe, "-m", "pip", "install", *packages, "--upgrade", "-y"])
    except subprocess.CalledProcessError as e:
        print("Error installing packages:", e)
    except Exception as e:
        print("Generic error", e)


install_modules(["astropy"])
