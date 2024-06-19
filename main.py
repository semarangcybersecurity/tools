# main.py

from assets.shell import Shell
from plugins.wpbf import wpbf
from scanner.shell import ShellScanner
from assets.colors import *

if __name__ == "__main__":
    shell = Shell()

    # Register wpbf plugin
    wp_enum = wpbf()
    shell.reg_plugin("wordpress_bruteforce", wp_enum, "Perform brute force attacks on WordPress sites to identify weak credentials.")

    # Register ShellScanner plugin
    shell_scanner = ShellScanner()
    shell.reg_plugin("shell_scanner", shell_scanner, "Find potential shells on a server.")

    print(banners.banner)
    shell.shell()
