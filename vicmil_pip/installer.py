"""
This is the installer that contains all information for how to install things
"""

import platform
import inspect
import zipfile
import os
import pathlib
import shutil
import importlib
import sys
import urllib.request
import subprocess
from typing import Dict
import time
sys.path.append(str(pathlib.Path(__file__).resolve().parents[0])) 

"""
=============================================================================
                                   Packages
=============================================================================
"""


def get_installed_packages_list():
    # List all the packages and print their description
    dirs = os.listdir(get_directory_path(__file__, 0) + "/lib")
    folders = list()
    for f in dirs:
        if f == "__pycache__":
            continue
        if f == "venv":
            continue
        folders.append(f)

    return folders


def print_installed_packages():
    folders = get_installed_packages_list()
    print(f"found {len(folders)} installed packages")
    print(folders)


def install_package(package_name: str):
    package_path = get_directory_path(__file__, 0) + "/lib/" + package_name
    if os.path.exists(package_path):
        print(f"Package {package_name} path already exists")
        return

    # Get the github repo path
    github_repo_main =   f"https://github.com/vicmil-pip-v2/{package_name}/archive/refs/heads/main.zip"
    github_repo_master = f"https://github.com/vicmil-pip-v2/{package_name}/archive/refs/heads/master.zip"

    # Download the package and unzip it
    tmp_zip = get_directory_path(__file__, 0) + "/temp.zip"

    download_github_repo_as_zip(github_repo_main, tmp_zip)
    if not os.path.exists(tmp_zip):
        download_github_repo_as_zip(github_repo_master, tmp_zip)

    if not os.path.exists(tmp_zip):
        print("Download failed, could not find url!")
        return
        
    # Create the package directory
    os.makedirs(package_path, exist_ok=True)

    unzip_without_top_dir(tmp_zip, package_path, delete_zip=True)

    # Install other vicmil-pip dependencies
    vicmil_pip_requirements_path = f"{package_path}/vicmil_pip_requirements.txt"
    if os.path.exists(vicmil_pip_requirements_path):
        with open(vicmil_pip_requirements_path, "r") as file:
            requirements_content = file.read()
            requirements_content: list = requirements_content.split("\n")
            for requirement in requirements_content:
                install_package(requirement)

    if os.path.exists(f"{package_path}/setup.py"):
        run_command(f'"{sys.executable}" "{package_path}/setup.py"')

    print("Succesfully installed package", package_name)


def clone_package(package_name: str):
    package_path = get_directory_path(__file__, 0) + "/lib/" + package_name
    if os.path.exists(package_path):
        print(f"Package {package_name} path already exists")
        return

    github_repo = f"git@github.com:vicmil-pip-v2/{package_name}.git"

    run_command(f'git clone "{github_repo}" "{package_path}"')

def remove_package(package_name: str):
    # Determine if the install is valid
    package_path = get_directory_path(__file__, 0) + "/lib/" + package_name
    if os.path.exists(package_path):
        # Remove package
        delete_folder_with_contents(package_path)
        print(f"removed package {package_name}")


"""
=============================================================================
                            Utility functions
=============================================================================
"""


def get_directory_path(__file__in, up_directories=0):
    return str(pathlib.Path(__file__in).parents[up_directories].resolve()).replace("\\", "/")


def delete_file(file: str):
    if os.path.exists(file):
        os.remove(file)


def delete_folder_with_contents(file: str):
    if os.path.exists(file):
        shutil.rmtree(file)  # Deletes the folder and its contents


def unzip_without_top_dir(zip_file_path, destination_folder, delete_zip=False):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Get the list of file paths in the zip
        members = zip_ref.namelist()
        
        # Identify the top-level directory (assume first path element)
        top_level_dir = os.path.commonprefix(members).rstrip('/')
        
        for member in members:
            # Remove the top-level directory from the file path
            relative_path = os.path.relpath(member, top_level_dir)
            
            # Compute the final extraction path
            final_path = os.path.join(destination_folder, relative_path)

            if member.endswith('/'):  # Handle directories
                os.makedirs(final_path, exist_ok=True)
            else:  # Extract files
                os.makedirs(os.path.dirname(final_path), exist_ok=True)
                with zip_ref.open(member) as src, open(final_path, 'wb') as dst:
                    dst.write(src.read())

    if delete_zip:
        delete_file(zip_file_path)


def get_venv_pip_path(env_directory_path):
    if platform.system() == "Windows":
        return f'{env_directory_path}/Scripts/pip'
    else:
        return f'{env_directory_path}/bin/pip'
    

def pip_install_packages_in_virtual_environment(env_directory_path, packages):
    if not os.path.exists(env_directory_path):
        print("Invalid path")
        raise Exception("Invalid path")
    
    for package in packages:
        run_command(f'"{get_venv_pip_path(env_directory_path)}" install {package}')
             

def python_virtual_environment(env_directory_path):
    # Setup a python virtual environmet
    os.makedirs(env_directory_path, exist_ok=True) # Ensure directory exists
    run_command(f'"{sys.executable}" -m venv "{env_directory_path}"')


def run_command(command: str) -> None:
    """Run a command in the terminal"""
    if platform.system() == "Windows": # Windows
        win_command = None
        if command[0] != '"':
            win_command = f'powershell; {command}'
        else:
            win_command = f'powershell; &{command}'

        print("running command: ", f'{win_command}')
        os.system(win_command)
    else:
        print("running command: ", f'{command}')
        os.system(command)


def get_venv_site_packages_path(venv_path):
    """Returns the site-packages path for a given virtual environment."""
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    
    # Construct the expected site-packages path
    if platform.system() == "Windows": # Windows
        # The site package path may vary on windows, so we check for both
        site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
        if not os.path.exists(site_packages_path):
            site_packages_path = os.path.join(venv_path, "lib", python_version, "site-packages")
    else:  # macOS/Linux
        site_packages_path = os.path.join(venv_path, "lib", python_version, "site-packages")

    return site_packages_path if os.path.exists(site_packages_path) else None


def module_installed(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False
    

def include_other_venv(other_venv_path: str):
    site_package_path = get_venv_site_packages_path(other_venv_path)
    if not other_venv_path in sys.path:
        print("Updating sys.path with other venv", site_package_path)
        sys.path.append(site_package_path)  # Add other venv's site-packages to sys.path
    

class PipManager:
    def __init__(self):
        self._modules = list()
        self.venv_path = get_directory_path(__file__) + "/venv"
        self.installed_pip_packages = list()

    def add_module(self, module_name: str, pip_package_if_missing: str):
        self._modules.append((module_name, pip_package_if_missing))

    def add_pip_package(self, pip_package: str):
        self._modules.append((None, pip_package))

    def include_other_venv(self):
        include_other_venv(self.venv_path)

    def install_missing_modules(self):
        """
        [vmdoc:start]
        # PipManager.install_missing_modules()

        Tries to see if the module is available, 
            if it fails, it installs the missing pip packages inside self.venv_path
        [vmdoc:end]
        """
        missing_pip_packages = set()

        for module_name, pip_package in self._modules:
            if not module_name or not module_installed(module_name=module_name):
                if not pip_package in self.installed_pip_packages:
                    missing_pip_packages.add(pip_package)
                    self.installed_pip_packages.append(pip_package)

        if len(missing_pip_packages) > 0:
            if not os.path.exists(self.venv_path):
                python_virtual_environment(self.venv_path)

            missing_pip_packages = list(missing_pip_packages)
            pip_install_packages_in_virtual_environment(self.venv_path, missing_pip_packages)

            self.include_other_venv()


def download_file(url, output_path, remove_existing_file=False):
    """
    Download a file from a URL with a single-line progress bar showing percentage
    and human-readable sizes. Optionally removes the output file if it already exists.
    If the file size is unknown, it prints "unknown size".
    
    Args:
        url (str): URL of the file to download.
        output_path (str): Path to save the downloaded file.
        remove_existing_file (bool): If True, removes the file if it exists before downloading.
    """
    import requests
    import sys
    import os

    # Remove existing file if requested
    if remove_existing_file and os.path.exists(output_path):
        os.remove(output_path)

    def human_readable(size):
        """Convert bytes to a human-readable string with correct units."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:6.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = response.headers.get('content-length')
    total_size = int(total_size) if total_size else None

    downloaded = 0
    chunk_size = 1024  # 1 KB
    bar_length = 50    # progress bar length

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)

                if total_size:
                    percent = downloaded / total_size
                    filled_length = int(bar_length * percent)
                    bar = '=' * filled_length + '-' * (bar_length - filled_length)
                    sys.stdout.write(
                        f"\r[{bar}] {percent*100:6.2f}% "
                        f"({human_readable(downloaded)} / {human_readable(total_size)})"
                    )
                else:
                    # File size unknown
                    filled_length = min(bar_length, downloaded // chunk_size)
                    bar = '=' * filled_length + '-' * (bar_length - filled_length)
                    sys.stdout.write(
                        f"\r[{bar}] Downloaded {human_readable(downloaded)} / unknown size"
                    )

                sys.stdout.flush()

    print("\nDownload complete!")


def download_github_repo_as_zip(zip_url: str, output_zip_file: str):
    """Downloads a GitHub repository as a ZIP file.
    
    Args:
        repo_url (str): The URL of the GitHub repository (e.g., "https://github.com/owner/repo").
        output_file (str): The name of the output ZIP file (e.g., "repo.zip").
    """
    try:
        pip_manager = PipManager()
        if not module_installed("requests"):
            pip_manager.add_pip_package("requests")
            pip_manager.install_missing_modules()

        download_file(url=zip_url, output_path=output_zip_file, remove_existing_file=True)
        
        # print(f"Download complete: {output_zip_file}")
    except Exception as e:
        #print(f"Error: {e}")
        pass