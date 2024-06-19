# shell_scanner.py

import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor
from assets.colors import *

x = "=" * 40

class ShellScanner:
    def __init__(self):
        self.options = {
            "TARGET_FILE": {"value": None, "required": True, "Description": "The target file containing list of URLs"},
            "DIR_LIST_FILE": {"value": "assets/files/dir.txt", "required": True, "Description": "File containing list of directories"},
            "FILE_LIST_FILE": {"value": "assets/files/nameshell.txt", "required": True, "Description": "File containing list of shell files"},
            "NUM_THREADS": {"value": 10, "required": False, "Description": "Number of concurrent threads"}
        }

    def set_options(self, option, value):
        if option in self.options:
            self.options[option]["value"] = value
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] Unknown option: {option}")

    def show_option(self):
        print(f" Plugins option ({self.__class__.__name__})")
        print()
        print(f" {'Name':<20} {'Current Setting':<30} {'Required':<10} {'Description'}")
        print(f" {'-'*20} {'-'*30} {'-'*10} {'-'*40}")
        for option, details in self.options.items():
            current_setting = details["value"] if details["value"] is not None else ""
            print(f" {option:<20} {current_setting:<30} {str(details['required']):<10} {details['Description']}")

    def get_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"[{colors.blue}Info{colors.reset}] File not found: {file_path}")
        except Exception as e:
            print(f"[{colors.red}Error{colors.reset}] An error occurred while loading file: {file_path}", e)

    def scan_directories(self, target_url, directories, current_path=""):
        try:
            with ThreadPoolExecutor(max_workers=int(self.options["NUM_THREADS"]["value"])) as executor:
                futures = [executor.submit(self.scan_directory, target_url, directory, current_path) for directory in directories]

            for future in futures:
                future.result()

        except requests.exceptions.RequestException as e:
            print(f"[{colors.red} ! {colors.reset}] An error occurred:", e)

    def scan_directory(self, target_url, directory, current_path):
        dir_path = os.path.join(current_path, directory)
        url = f"{target_url}/{dir_path}"

        try:
            response = requests.head(url, verify=True)
        except requests.exceptions.SSLError:
            url = url.replace("https://", "http://")
            response = requests.head(url, verify=False)

        if response.status_code == 403:
            print(f"[{colors.green}✔{colors.reset}] Directory: {url}")
            self.scan_files(target_url, directory, current_path)
        elif response.status_code == 200:
            print(f"[{colors.cyan}❔{colors.reset}] Directory: {url}")
            self.scan_files(target_url, directory, current_path)
        elif response.status_code == 301:
            print(f"[{colors.yellow}❔{colors.reset}] Directory: {url}")
        else:
            print(f"[{colors.red}✗{colors.reset}] Directory: {url}")

    def scan_files(self, target_url, directory, current_path):
        file_list = self.get_file(self.options["FILE_LIST_FILE"]["value"])
        if file_list:
            with ThreadPoolExecutor(max_workers=int(self.options["NUM_THREADS"]["value"])) as executor:
                futures = [executor.submit(self.scan_file, target_url, file, directory, current_path) for file in file_list]

            for future in futures:
                future.result()

    def scan_file(self, target_url, file, directory, current_path):
        file_path = os.path.join(current_path, directory, file)
        url = f"{target_url}/{file_path}"

        try:
            response = requests.head(url, verify=True)
        except requests.exceptions.SSLError:
            url = url.replace("https://", "http://")
            response = requests.head(url, verify=False)

        if response.status_code == 200:
            print(f"[{colors.yellow}✔{colors.reset}] File: {url}")
        else:
            print(f"[{colors.red}✗{colors.reset}] File: {url}")

    def start_scan(self):
        target_file = self.options["TARGET_FILE"]["value"]
        if not target_file:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] Please set the TARGET_FILE option.")
            return

        target_urls = self.get_file(target_file)
        dir_list_file = self.options["DIR_LIST_FILE"]["value"]

        for target_url in target_urls:
            print(f"\nScanning target:{colors.blue} {target_url}{colors.reset}")
            print(x)
            dir_list = self.get_file(dir_list_file)
            if dir_list:
                self.scan_directories(target_url, dir_list)

    def run(self):
        self.start_scan()

    def help(self):
        print("This is the Shell Scanner plugin.")
        print("Options:")
        self.show_option()
        print("\nCommands:")
        print("  set [option] [value]    - Set an option")
        print("  show                    - Show current options")
        print("  exploit / run           - Run the scan")
        print("  help                    - Show this help message")
        print("  use [plugin]            - Select a plugin to use")
        print("  exit                    - Exit the shell")
