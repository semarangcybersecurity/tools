# shell.py

from assets.colors import *

class Shell:
    def __init__(self):
        self.plugins = {}
        self.plugin_descriptions = {}
        self.current_plugin = None
    
    def reg_plugin(self, name, plugin, description):
        self.plugins[name] = plugin
        self.plugin_descriptions[name] = description
    
    def set_options(self, option, value):
        if self.current_plugin:
            self.current_plugin.set_options(option, value)
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] No plugin selected...")
    
    def show_option(self):
        if self.current_plugin:
            self.current_plugin.show_option()
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] No plugin selected...")
    
    def run(self):
        if self.current_plugin:
            self.current_plugin.run()
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] No plugin selected...")
    
    def help(self):
        if self.current_plugin:
            self.current_plugin.help()
        else:
            print(f"{colors.white}[{colors.magenta}✔{colors.white}] Available plugins:")
            for plugin, description in self.plugin_descriptions.items():
                print(f" - {plugin}: {description}")
            print("\nGeneral commands:")
            print("  show                    - Show current options")
            print("  set [option] [value]    - Set an option")
            print("  exploit / run           - Run the selected plugin")
            print("  use [plugin]            - Select a plugin to use")
            print("  help                    - Show this help message")
            print("  exit                    - Exit the shell")
    
    def use(self, plugin_name):
        if plugin_name in self.plugins:
            self.current_plugin = self.plugins[plugin_name]
            print(f"{colors.white}[{colors.green}✔{colors.white}] Using plugin : {plugin_name}")
        else:
            print(f"{colors.white}[{colors.darkred}✗{colors.white}] Plugin {plugin_name} not found.")
    
    def shell(self):
        while True:
            if self.current_plugin:
                plugin_name = self.current_plugin.__class__.__name__
                command = input(f"{colors.white}ETHOPIA ({colors.darkred}{plugin_name}{colors.white}) > ").strip().split()
            else:
                command = input(f"{colors.white}ETHOPIA > ").strip().split()
                
            if not command:
                continue
            cmd = command[0].lower()
            args = command[1:]
            if cmd == "show":
                if len(args) == 1 and args[0] == "plugins":
                    self.show_plugins()
                else:
                    self.show_option()
            elif cmd == "set":
                if len(args) != 2:
                    print(f"{colors.white}[{colors.darkred}✗{colors.white}] Usage : set [option] [value]")
                else:
                    self.set_options(args[0], args[1])
            elif cmd in ["exploit", "run"]:
                self.run()
            elif cmd == "help":
                self.help()
            elif cmd == "use":
                if len(args) != 1:
                    print(f"{colors.white}[{colors.darkred}✗{colors.white}] Usage : use [plugin]")
                else:
                    self.use(args[0])
            elif cmd == "exit":
                break
            else:
                print(f"{colors.white}[{colors.darkred}✗{colors.white}] Unknown command : {cmd}")
    
    def show_plugins(self):
        print(f"{colors.white}[{colors.magenta}✔{colors.white}] Available plugins:")
        for plugin, description in self.plugin_descriptions.items():
            print(f" - {plugin}: {description}")
