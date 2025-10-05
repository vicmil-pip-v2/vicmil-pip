"""
# Info
vicmil_pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

# Getting started
python vicmil_pip.py help 
    or
python3 vicmil_pip.py help 

# Documentation (Coming soon)
https://vicmil_pip.com



# More details
When you install something, a map called vicmil_pip/ will be created, where all packages
    you install will be stored. Nothing external will be installed on your computer.

The idea is for all the packages to be cross-platform(windows, linux, mac), so the thing
    that actually gets installed may vary depending on platform. The idea is for all packages 
    to use a permissive licence, so they can be used in commercial applications. Read more
    about specific packages at: https://vicmil_pip.com

You can also opt-out of using vicmil_pip but still use the packages by navigating to
    https://vicmil_pip.com, there you will find install instructions for installing
    the packages manually and read more about where they came from.

This is the main file, and the only thing you need to use vicmil_pip
"""

import sys
import pathlib
import os
import urllib.request


def get_directory_path(__file__in, up_directories=0):
    return str(pathlib.Path(__file__in).parents[up_directories].resolve()).replace("\\", "/")


def install_installer():
    vicmil_pip_path = get_directory_path(__file__, 0) + "/vicmil_pip"
    if not os.path.exists(vicmil_pip_path):
        os.makedirs(vicmil_pip_path, exist_ok=True)

    if not os.path.exists(vicmil_pip_path + "/packages"):
        os.makedirs(vicmil_pip_path, exist_ok=True)

    with open(vicmil_pip_path + "/__init__.py", "w") as _: # Create the init file
        pass

    with open(vicmil_pip_path + "/.gitignore", "w") as file_: # Create the gitignore file
        file_.write("__pycache__*\nvenv/")

    with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil_pip/vicmil_pip/refs/heads/main/vicmil_pip/installer.py') as f:
        html = f.read().decode('utf-8')
        with open(vicmil_pip_path + "/installer.py", "w") as install_file: # Create install file
            install_file.write(html)

    if not os.path.exists(vicmil_pip_path+ "/venv"):
        import vicmil_pip.installer as vicmil_pip_installer
        vicmil_pip_installer.python_virtual_environment(vicmil_pip_path + "/venv")
        vicmil_pip_installer.pip_install_packages_in_virtual_environment(vicmil_pip_path + "/venv", ["gdown"])


def installer_exists():
    vicmil_pip_path = get_directory_path(__file__, 0) + "/vicmil_pip"
    if os.path.exists(vicmil_pip_path + "/installer.py"):
        return True
    return False


def update_vicmil_pip():
    # Download the latest features into this file
    with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil_pip/vicmil_pip/refs/heads/main/vicmil_pip.py') as f:
        html = f.read().decode('utf-8')
        with open(__file__, "w") as this_file: # Create install file
            this_file.write(html)


if __name__ == "__main__":
    arguments: list = sys.argv[1:]
    print(arguments)

    if len(arguments) == 0 or arguments[0] == "help":
        help_str = \
"""
vicmil_pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

Visit https://vicmil.uk/pip for more info

Commands:
python3 vicmil_pip.py help // prints help and info
python3 vicmil_pip.py update // updates vicmil-pip to latest version
python3 vicmil_pip.py install ... // Install a package
python3 vicmil_pip.py remove ... // remove a package
python3 vicmil_pip.py install -r vicmil-requirements.txt // install all vicmil packages listed in file
python3 vicmil_pip.py list // lists installed vicmil packages
python3 vicmil_pip.py packages // list all available packages with more info
"""
        print(help_str)
        exit(0)

    if arguments[0] == "install":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer as vicmil_pip_installer

        if len(arguments) == 2 and arguments[1] == "-r":
            print("You need to specify a file to install from file")

        if len(arguments) > 2 and arguments[1] == "-r":
            print("Installing from requirements file")
            # open file and iterate through it line by line
            # install each package on each line
            filename = arguments[2]
            try:
                with open(filename, "r") as file:
                    for line in file:
                        vicmil_pip_installer.install_package(line.strip(), debug=False)

            except FileNotFoundError:
                print(f"Error: The file '{filename}' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

            print("Done!")

        elif len(arguments) > 1:
            vicmil_pip_installer.install_package(arguments[1])

    if arguments[0] == "force-install":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer as vicmil_pip_installer

        if len(arguments) > 1:
            vicmil_pip_installer.remove_package(arguments[1])
            vicmil_pip_installer.install_package(arguments[1])

    if arguments[0] == "clone":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer as vicmil_pip_installer

        if len(arguments) > 1:
            vicmil_pip_installer.clone_package(arguments[1])
        
    if arguments[0] == "update":
        print("upgrade vicmil_pip/installer.py")
        install_installer()
        print("upgrade current file")
        update_vicmil_pip()

    if arguments[0] == "remove":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer as vicmil_pip_installer

        if len(arguments) > 1:
            vicmil_pip_installer.remove_package(arguments[1])

    if arguments[0] == "list":
        if not installer_exists():
            print("Installer does not exist, install installer")
            install_installer()

        import vicmil_pip.installer as vicmil_pip_installer

        vicmil_pip_installer.print_installed_packages()
